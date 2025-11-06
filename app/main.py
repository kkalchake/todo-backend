# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_tasks import router as task_router
from app.db.database import Base, engine

app = FastAPI(title="Todo Backend API")

# Define the allowed origins for CORS
# 1. Frontend URL (where the browser is running)
# 2. Backend URL (often needed for Codespace internal consistency/testing)
origins = [
    "https://literate-engine-g4vgp59v74q29r5j-3000.app.github.dev",
    "https://refactored-umbrella-4jw99977qq442qq67-8000.app.github.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the corrected list of origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],    # Allows all headers
)

# Initialize the database structure
Base.metadata.create_all(bind=engine)

# Include the application router
app.include_router(task_router)