from sqlalchemy.orm import Session
from app.models.domain import Task, Status
from app.models.schemas import TaskCreate, TaskUpdate
from datetime import datetime

class TaskRepository:

    def get_all(self, db: Session):
        return db.query(Task).all()

    def get(self, db: Session, task_id: str):
        return db.query(Task).filter(Task.id == task_id).first()

    def add(self, db: Session, task: TaskCreate):
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def delete(self, db: Session, task_id: str):
        db_task = self.get(db, task_id)
        if not db_task:
            return None
        db.delete(db_task)
        db.commit()
        return True

    def update(self, db: Session, task_id: str, task_update: TaskUpdate):
        db_task = self.get(db, task_id)
        if not db_task:
            return None
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
        return db_task
