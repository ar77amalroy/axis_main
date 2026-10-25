"""Base interface for all agents."""


async def run(instruction: str, context: str = "") -> dict:
    """Override in concrete agents.  Returns {"status": "done"|"failed", "result": str}."""
    raise NotImplementedError("Subclasses must implement run()")
