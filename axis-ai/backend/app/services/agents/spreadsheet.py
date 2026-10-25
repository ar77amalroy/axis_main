"""Spreadsheet agent stub – delegates to LLM with a spreadsheet-specialist prompt."""

from app.services.llm import chat_text

ROLE = "You are a spreadsheet assistant. Produce concise data summaries, formulas, or table layouts."


async def run(instruction: str, context: str = "") -> dict:
    prompt = instruction
    if context:
        prompt += f"\n\nPrevious step context:\n{context}"
    try:
        result = await chat_text(ROLE, prompt)
        return {"status": "done", "result": result}
    except Exception as exc:
        return {"status": "failed", "result": str(exc)}
