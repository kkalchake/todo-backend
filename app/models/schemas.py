from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None

class TaskResponse(TaskBase):
    id: str
    status: Status
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
