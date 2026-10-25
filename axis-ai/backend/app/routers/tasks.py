from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from app.db import tasks_col, workflow_steps_col
from app.deps import get_current_user
from app.models.task import TaskCreate, TaskOut, TaskInDB
from app.models.workflow_step import WorkflowStepOut
from app.services.orchestrator import run_orchestrator

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _doc_to_out(doc: dict) -> TaskOut:
    return TaskOut(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        command_text=doc["command_text"],
        input_mode=doc["input_mode"],
        file_ids=doc.get("file_ids", []),
        status=doc["status"],
        created_at=doc["created_at"],
    )


def _step_to_out(doc: dict) -> WorkflowStepOut:
    return WorkflowStepOut(
        id=str(doc["_id"]),
        task_id=doc["task_id"],
        step_index=doc["step_index"],
        agent=doc.get("agent", ""),
        instruction=doc.get("instruction", ""),
        status=doc["status"],
        result=doc.get("result"),
        created_at=doc["created_at"],
        finished_at=doc.get("finished_at"),
    )


@router.post("", response_model=TaskOut, status_code=201)
async def create_task(
    body: TaskCreate,
    bg: BackgroundTasks,
    user: dict = Depends(get_current_user),
):
    doc = TaskInDB(
        user_id=user["id"],
        command_text=body.command_text,
        input_mode=body.input_mode,
        file_ids=body.file_ids,
    ).model_dump()

    result = await tasks_col.insert_one(doc)
    doc["_id"] = result.inserted_id

    # Fire orchestrator in the background – return task immediately as pending
    bg.add_task(run_orchestrator, str(result.inserted_id))

    return _doc_to_out(doc)


@router.get("", response_model=List[TaskOut])
async def list_tasks(user: dict = Depends(get_current_user)):
    cursor = tasks_col.find({"user_id": user["id"]}).sort("created_at", -1)
    return [_doc_to_out(d) async for d in cursor]


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: str, user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid task ID")

    doc = await tasks_col.find_one({"_id": ObjectId(task_id), "user_id": user["id"]})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    return _doc_to_out(doc)


@router.get("/{task_id}/steps", response_model=List[WorkflowStepOut])
async def get_task_steps(task_id: str, user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid task ID")

    # Verify task ownership
    task = await tasks_col.find_one({"_id": ObjectId(task_id), "user_id": user["id"]})
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    cursor = workflow_steps_col.find({"task_id": task_id}).sort("step_index", 1)
    return [_step_to_out(d) async for d in cursor]
