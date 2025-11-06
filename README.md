# Todo Backend API

A modular and extensible backend for managing tasks using FastAPI, SQLAlchemy, and Pydantic. 
Built with intention for a clean architecture for testability, maintainability, and future production readiness.

## Features

- FastAPI-based REST API
- SQLAlchemy ORM with Pydantic validation
- Layered architecture with service and repository abstraction
- In-memory SQLite test database for fast and isolated testing
- Automated tests using Pytest

## Requirements

- Python 3.11 or higher
- pip (Python package manager)
- Optional: virtualenv

## Local Setup

```bash
git clone https://github.com/kkalchake/todo-backend.git
cd todo-backend
python3 -m venv venv
source venv/bin/activate # For Windows: venv\Scripts\activate
pip install -r requirements.txt

## Running the API
```bash
uvicorn app.main:app --reload
Server will be available at:

Base URL: http://localhost:8000

## API Endpoints
POST /tasks — Create a new task
GET /tasks — Retrieve all tasks
PUT /tasks/{id} — Update a task
DELETE /tasks/{id} — Delete a task

## Running Tests
```bash
pytest or PYTHONPATH=. pytest

## Generate coverage report:
```bash
pip install pytest-cov
pytest --cov=app tests/

## Task Object Format
{
  "id": "uuid",
  "title": "Task title",
  "description": "Optional details",
  "status": "PENDING",
  "created_at": "2025-11-05T18:55:00Z",
  "updated_at": "2025-11-05T18:55:00Z"
}

## Manual Functional Testing
Example with curl:
```bash
curl -X POST http://localhost:8000/tasks/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Test task", "description": "Manual test"}'

To verify:
```bash
curl http://localhost:8000/tasks/

-------------------------------------
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

## Collaboration: Dockerization and CI/CD
Docker and CI/CD are not yet implemented.

Suggested enhancements for collaborators:

Add a Dockerfile to containerize the FastAPI backend

Add a docker-compose.yml for backend + PostgreSQL integration

Implement GitHub Actions for automated testing and build verification

Prepare deployment configuration for Render, Fly.io, or AWS ECS

Developers are encouraged to fork the repository, create feature branches, and open pull requests with detailed descriptions.