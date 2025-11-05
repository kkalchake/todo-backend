from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime, UTC
import uuid

class Status(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"

def now_utc():
    return datetime.now(UTC)

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None