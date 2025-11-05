from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.repository import TaskRepository
from app.models import Task, TaskCreate, TaskUpdate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://refactored-umbrella-4jw99977qq442qq67-8000.app.github.dev",  # Allows all Codespaces URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
repo = TaskRepository()

def get_repo():
    return repo

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, repo: TaskRepository = Depends(get_repo)):
    new_task = Task(**task.model_dump())
    return repo.add(new_task)

@app.get("/tasks", response_model=list[Task])
def list_tasks(repo: TaskRepository = Depends(get_repo)):
    return repo.get_all()

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, repo: TaskRepository = Depends(get_repo)):
    try:
        repo.delete(task_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update: TaskUpdate, repo: TaskRepository = Depends(get_repo)):
    try:
        return repo.update(task_id, **update.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")