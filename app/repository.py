import json
from typing import List, Optional
from app.models import Task
from pathlib import Path

class TaskRepository:
    def __init__(self, file_path: Path = Path("tasks.json")):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.file_path = file_path
        self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                self.tasks = [Task(**t) for t in json.load(f)]
        else:
            self.tasks = []

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump([t.model_dump() for t in self.tasks], f, default=str, indent=2)

    def add(self, task: Task) -> Task:
        self.tasks.append(task)
        self._save()
        return task

    def get_all(self) -> List[Task]:
        return self.tasks

    def get(self, task_id: str) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def delete(self, task_id: str) -> None:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) == before:
            raise ValueError("Task not found")
        self._save()

    def update(self, task_id: str, **kwargs) -> Task:
        task = self.get(task_id)
        if not task:
            raise ValueError("Task not found")
        for k, v in kwargs.items():
            if v is not None:
                setattr(task, k, v)
        task.updated_at = task.updated_at.now()
        self._save()
        return task