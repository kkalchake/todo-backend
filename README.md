# FastAPI To-Do Backend

A production-ready, modular, and fully tested to-do list backend using FastAPI and Python.

## Features

- RESTful API: Create, list, update, and delete tasks
- File-based persistence (`tasks.json`)
- Clean, extensible architecture
- Fully tested with `pytest`

## Setup

```bash
git clone <YOUR_REPO_URL>
cd todo-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Running the API
uvicorn app.main:app --reload
API will be available at http://127.0.0.1:8000 

## API Endpoints
POST /tasks — Add a new task
GET /tasks — List all tasks
PUT /tasks/{id} — Update a task
DELETE /tasks/{id} — Delete a task

## Running Tests
pytest or PYTHONPATH=. pytest

## Project Structure
app/models.py — Data models
app/repository.py — Persistence layer
app/main.py — API routes
tests/ — Unit tests

## API Testing
You can use Postman or CLI to interact with the API.

1. Create a Task
Method: POST
URL: http://127.0.0.1:8000/tasks
Body (JSON):
{
  "title": "Sample Task",
  "description": "This is a test"
}

2. List All Tasks
Method: GET
URL: http://127.0.0.1:8000/tasks

3. Update a Task
Method: PUT
URL: http://127.0.0.1:8000/tasks/{id}
Body (JSON):
{
  "title": "Updated Title",
  "status": "COMPLETED"
}

Replace {id} with the actual task ID from the list endpoint.

4. Delete a Task
Method: DELETE
URL: http://127.0.0.1:8000/tasks/{id}
Replace {id} with the actual task ID from the list endpoint.

