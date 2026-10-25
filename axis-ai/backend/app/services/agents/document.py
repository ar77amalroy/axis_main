"""Document agent stub – delegates to LLM with a document-specialist prompt."""

from app.services.llm import chat_text

ROLE = "You are a document-editing assistant. Produce concise, professional text."


async def run(instruction: str, context: str = "") -> dict:
    prompt = instruction
    if context:
        prompt += f"\n\nPrevious step context:\n{context}"
    try:
        result = await chat_text(ROLE, prompt)
        return {"status": "done", "result": result}
    except Exception as exc:
        return {"status": "failed", "result": str(exc)}
