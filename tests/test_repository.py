import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.repository import TaskRepository
from app.db.database import Base
from app.models.schemas import TaskCreate

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_add_and_get_task(db):
    repo = TaskRepository()
    task_in = TaskCreate(title="Repo Task", description="Test repo")
    task = repo.add(db, task_in)

    fetched = repo.get(db, task.id)
    assert fetched is not None
    assert fetched.title == "Repo Task"

def test_delete_task(db):
    repo = TaskRepository()
    task = repo.add(db, TaskCreate(title="To Delete"))
    repo.delete(db, task.id)

    assert repo.get(db, task.id) is None
