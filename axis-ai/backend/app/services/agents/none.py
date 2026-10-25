"""None agent – always fails with the given reason."""


async def run(instruction: str, context: str = "") -> dict:
    return {"status": "failed", "result": instruction}
