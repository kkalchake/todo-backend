def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Desc"
    assert "id" in data
    assert "created_at" in data
    assert data["status"] == "PENDING"

def test_list_tasks(client):
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Adjust depending on isolation

def test_update_task(client):
    create_resp = client.post("/tasks/", json={"title": "Original"})
    task_id = create_resp.json()["id"]

    update_resp = client.put(f"/tasks/{task_id}", json={"title": "Updated", "status": "COMPLETED"})
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["title"] == "Updated"
    assert updated["status"] == "COMPLETED"

def test_delete_task(client):
    create_resp = client.post("/tasks/", json={"title": "Delete Me"})
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get("/tasks/")
    assert task_id not in [t["id"] for t in get_resp.json()]
