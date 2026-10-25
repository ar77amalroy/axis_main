from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    command_text: str
    input_mode: Literal["text", "voice"] = "text"
    file_ids: List[str] = []


class TaskOut(BaseModel):
    id: str
    user_id: str
    command_text: str
    input_mode: Literal["text", "voice"]
    file_ids: List[str]
    status: Literal["pending", "running", "completed", "failed"]
    created_at: datetime


class TaskInDB(BaseModel):
    user_id: str
    command_text: str
    input_mode: Literal["text", "voice"] = "text"
    file_ids: List[str] = []
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
