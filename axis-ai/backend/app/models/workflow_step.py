from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WorkflowStepOut(BaseModel):
    id: str
    task_id: str
    step_index: int
    agent: str = ""
    instruction: str = ""
    status: str
    result: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None


class WorkflowStepInDB(BaseModel):
    task_id: str
    step_index: int
    agent: str = ""
    instruction: str = ""
    status: str = "pending"
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None
