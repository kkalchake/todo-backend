from sqlalchemy.orm import Session
from app.db.repository import TaskRepository
from app.models.schemas import TaskCreate, TaskUpdate

repo = TaskRepository()

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self):
        return repo.get_all(self.db)

    def create_task(self, task: TaskCreate):
        return repo.add(self.db, task)

    def update_task(self, task_id: str, task_update: TaskUpdate):
        return repo.update(self.db, task_id, task_update)

    def delete_task(self, task_id: str):
        return repo.delete(self.db, task_id)
