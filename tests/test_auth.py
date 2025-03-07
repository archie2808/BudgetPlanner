import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.database import SessionLocal, engine, get_db
from app.models import Base, User
from app.main import app

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create a test client using the FastAPI app
client = TestClient(app)

#Override the get db dependency to use SessionLocal
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

def test_signup_creates_user():
    #Define the test user credentials
    test_data = {
        "username": f"testuser {uuid.uuid4()}",
        "password": "testpassword"
    }
    # Send a POST request to the signup endpoint with JSON payload
    response = client.post("/users", json = test_data)