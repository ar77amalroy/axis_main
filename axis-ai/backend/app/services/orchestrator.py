"""
Orchestrator – Phase 2.
Calls the LLM planner, dispatches agent steps, tracks workflow_steps in Mongo.
"""

from datetime import datetime

from bson import ObjectId

from app.db import tasks_col, workflow_steps_col
from app.services.planner import plan_task
from app.services.agents.registry import get_agent


async def run_orchestrator(task_id: str) -> None:
    """Run the full plan-and-execute pipeline for a task."""
    try:
        oid = ObjectId(task_id)

        # 1. Mark task as running
        await tasks_col.update_one(
            {"_id": oid},
            {"$set": {"status": "running"}},
        )

        task = await tasks_col.find_one({"_id": oid})
        if not task:
            return

        command_text = task.get("command_text", "")
        file_names = task.get("file_ids", [])

        # 2. Call planner
        try:
            steps = await plan_task(command_text, file_names)
        except Exception as exc:
            await tasks_col.update_one(
                {"_id": oid},
                {"$set": {
                    "status": "failed",
                    "error": f"Planner error: {exc}",
                }},
            )
            return

        # 3. Execute each step
        any_failed = False
        prev_result = ""

        for idx, step in enumerate(steps):
            agent_name = step["agent"]
            instruction = step["instruction"]

            # Insert workflow_step doc
            step_doc = {
                "task_id": task_id,
                "step_index": idx,
                "agent": agent_name,
                "instruction": instruction,
                "status": "running",
                "result": None,
                "created_at": datetime.utcnow(),
                "finished_at": None,
            }
            insert_res = await workflow_steps_col.insert_one(step_doc)
            step_oid = insert_res.inserted_id

            # Resolve agent
            agent_fn = get_agent(agent_name)
            if agent_fn is None:
                outcome = {"status": "failed", "result": f"Unknown agent: {agent_name}"}
            else:
                try:
                    outcome = await agent_fn(instruction, prev_result)
                except Exception as exc:
                    outcome = {"status": "failed", "result": str(exc)}

            # Update step
            await workflow_steps_col.update_one(
                {"_id": step_oid},
                {"$set": {
                    "status": outcome["status"],
                    "result": outcome.get("result", ""),
                    "finished_at": datetime.utcnow(),
                }},
            )

            if outcome["status"] == "failed":
                any_failed = True
                break  # stop pipeline on first failure

            prev_result = outcome.get("result", "")

        # 4. Final task status
        final_status = "failed" if any_failed else "completed"
        await tasks_col.update_one(
            {"_id": oid},
            {"$set": {"status": final_status}},
        )

    except Exception as exc:
        # Catch-all: any crash → task failed
        try:
            await tasks_col.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {
                    "status": "failed",
                    "error": f"Orchestrator crash: {exc}",
                }},
            )
        except Exception:
            pass
