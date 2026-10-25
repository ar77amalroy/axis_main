from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OutputOut(BaseModel):
    id: str
    task_id: str
    file_url: Optional[str] = None
    content: Optional[str] = None
    created_at: datetime


class OutputInDB(BaseModel):
    task_id: str
    file_url: Optional[str] = None
    content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
