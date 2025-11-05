import pytest
from fastapi.testclient import TestClient
from app.main import app, get_repo
from app.repository import TaskRepository
from pathlib import Path

TEST_FILE = "taskstest.json"

@pytest.fixture(autouse=True)
def cleanup():
    Path(TEST_FILE).unlink(missing_ok=True)

@pytest.fixture(autouse=True)
def override_repo():
    repo = TaskRepository(TEST_FILE)
    app.dependency_overrides[get_repo] = lambda: repo
    yield
    app.dependency_overrides = {}

client = TestClient(app)

def test_create_and_list_task():
    resp = client.post("/tasks", json={"title": "Test", "description": "Desc"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test"
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

def test_delete_task():
    resp = client.post("/tasks", json={"title": "ToDelete"})
    task_id = resp.json()["id"]
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    resp = client.get("/tasks")
    assert resp.json() == []

def test_update_task():
    resp = client.post("/tasks", json={"title": "ToUpdate"})
    task_id = resp.json()["id"]
    resp = client.put(f"/tasks/{task_id}", json={"title": "Updated", "status": "COMPLETED"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated"
    assert data["status"] == "COMPLETED"