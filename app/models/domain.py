from sqlalchemy import Column, String, Text, Enum, DateTime
from datetime import datetime, UTC
import uuid
import enum
from app.db.database import Base

class Status(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"

def now_utc():
    return datetime.now(UTC)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), default=Status.PENDING)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)
