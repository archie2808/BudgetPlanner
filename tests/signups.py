import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, User
from app.main import app, get_db

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
        "username": "testuser",
        "password": "testpassword"
    }
    # Send a POST request to the signup endpoint with JSON payload
    response = client.post("/auth/signup", json = test_data)

    # Verify the response status code is 200 ok 
    assert response.status_code == 200, f"Response: {response.text}"

    # Parse the JSON response and confirm it contains a user ID
    response_data = response.json()
    assert "USER_ID" in response_data,"UID NOT IN RESPONSE"

    # Verify the user was created in the database
    db: Session = next(override_get_db())
    user = db.query(User).filter(User.username == test_data["username"]).first()
    
    # Assert that a user was found and that the hashed password is stored (and different from the plain password)
    assert user is not None, "User not found in database"
    assert user.hashed_password != test_data["password"], "Stored password should be hashed"
