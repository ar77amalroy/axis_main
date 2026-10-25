"""Agent registry – maps agent name to its run() function."""

from app.services.agents import document, spreadsheet, presentation, none

AGENTS: dict[str, callable] = {
    "document": document.run,
    "spreadsheet": spreadsheet.run,
    "presentation": presentation.run,
    "none": none.run,
}


def get_agent(name: str):
    """Return the agent's run function, or None if unregistered."""
    return AGENTS.get(name)
