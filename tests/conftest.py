# conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool # Use StaticPool for the in-memory SQLite

from app.db.database import Base, get_db
from app.main import app

# --- 1. ENGINE FIX: Create the engine once for the entire session ---
# We use 'sqlite://' or 'sqlite:///:memory:' with StaticPool
# to ensure the in-memory DB is persistent throughout the entire test run.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    """Fixture to create the database engine for the test session."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        # StaticPool is crucial for in-memory SQLite to persist across threads/requests
        poolclass=StaticPool 
    )
    # The session scope means tables are created ONCE before any test
    Base.metadata.create_all(bind=engine)
    yield engine
    # Optional: Drop all tables after the entire test session (clean up)
    Base.metadata.drop_all(bind=engine)

# --- 2. SESSION FACTORY FIX: Create the session factory ---
@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    """Fixture to create the session local factory."""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# --- 3. ISOLATED DB FIX: This runs for every test (function scope) ---
@pytest.fixture(scope="function")
def db_session(TestingSessionLocal, test_engine):
    """
    Provides a clean, isolated database session for each test function.
    It uses a transaction that is rolled back at the end of the test.
    """
    # Begin a connection and transaction
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # Bind a new session to the connection
    db = TestingSessionLocal(bind=connection)
    
    try:
        yield db
    finally:
        # Roll back the transaction (undoing any changes made by the test)
        transaction.rollback()
        # Close the connection
        connection.close()


# --- 4. CLIENT FIX: Provides the TestClient using the isolated session ---
@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture to create a TestClient with the database dependency overridden.
    """
    # Override the app's 'get_db' dependency to use the isolated test session
    def override_get_db():
        try:
            yield db_session
        finally:
            # We don't close the session here; it's managed by db_session fixture cleanup
            pass 

    app.dependency_overrides[get_db] = override_get_db
    
    # Yield the client
    yield TestClient(app)
    
    # Clean up dependency override
    app.dependency_overrides.clear()