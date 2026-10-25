"""Planner – turns a user command into a list of agent steps via the LLM."""

from app.services.llm import chat_json

ALLOWED_AGENTS = {"document", "spreadsheet", "presentation", "none"}

SYSTEM_PROMPT = """\
You are a planner for office-productivity tasks.
Given a user command and optional file names, produce a JSON plan.

Allowed agents: "document", "spreadsheet", "presentation", "none".
Return EXACTLY this shape:
{"steps":[{"agent":"<agent>","instruction":"<what to do>"}]}

Rules:
- Maximum 5 steps.
- Use ONLY the allowed agents listed above.
- If the request is unclear, unsupported, or you cannot help, return ONE step
  with agent "none" and a short reason as the instruction.
- Do NOT include any text outside the JSON object.
"""


async def plan_task(command_text: str, file_names: list[str] | None = None) -> list[dict]:
    """Return a validated list of steps: [{"agent":..., "instruction":...}, ...]."""
    user_msg = f"Command: {command_text}"
    if file_names:
        user_msg += f"\nFiles: {', '.join(file_names)}"

    data = await chat_json(SYSTEM_PROMPT, user_msg)

    steps = data.get("steps", [])
    if not isinstance(steps, list):
        return [{"agent": "none", "instruction": "Planner returned invalid format."}]

    # Cap at 5 and filter unknown agents
    validated: list[dict] = []
    for s in steps[:5]:
        agent = s.get("agent", "").lower()
        instruction = s.get("instruction", "")
        if agent in ALLOWED_AGENTS:
            validated.append({"agent": agent, "instruction": instruction})

    if not validated:
        return [{"agent": "none", "instruction": "Planner produced no valid steps."}]

    return validated
