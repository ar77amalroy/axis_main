"""Presentation agent stub – delegates to LLM with a presentation-specialist prompt."""

from app.services.llm import chat_text

ROLE = "You are a presentation assistant. Produce concise slide outlines and talking points."


async def run(instruction: str, context: str = "") -> dict:
    prompt = instruction
    if context:
        prompt += f"\n\nPrevious step context:\n{context}"
    try:
        result = await chat_text(ROLE, prompt)
        return {"status": "done", "result": result}
    except Exception as exc:
        return {"status": "failed", "result": str(exc)}
