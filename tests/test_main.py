def test_create_task(client):
    """
    Test creating a new task successfully.
    """
    response = client.post("/tasks/", json={"title": "Write tests", "description": "Phase 2 QA"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["description"] == "Phase 2 QA"
    assert data["status"] == "PENDING"
    assert "id" in data
    assert "created_at" in data


def test_list_tasks(client):
    """
    Test listing all tasks. Ensures test isolation.
    """
    # Create 2 tasks *for this test*
    client.post("/tasks/", json={"title": "Task A"})
    client.post("/tasks/", json={"title": "Task B"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Because tests are isolated, we can be precise
    assert len(data) == 2
    assert any(task["title"] == "Task A" for task in data)


def test_update_task(client):
    """
    Test updating an existing task.
    """
    create = client.post("/tasks/", json={"title": "Original Title"})
    task_id = create.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Title", "status": "COMPLETED"})
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Updated Title"
    assert updated["status"] == "COMPLETED"


def test_delete_task(client):
    """
    Test deleting an existing task.
    """
    create = client.post("/tasks/", json={"title": "To Be Deleted"})
    task_id = create.json