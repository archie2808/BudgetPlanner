from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import SignupRequest, LoginRequest
from app.models import User         
from app.database import SessionLocal
from app.hashpassword import hash_password, verify_password
from app.database import get_db
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import annotated
import jwt
from jwt.exceptions import InvalidTokenError


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/users", status_code = status.HTTP_201_CREATED)
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint accepts a JSON body containing username and password. It first checks if a user
    with the given username already exists, and if not, hashes the password and creates a new user
    record in the database.

    Args:
        signup_data (SignupRequest): A Pydantic model containing the signup data (username and password).
        db (Session, optional): A SQLAlchemy session provided by the dependency injection.

    Raises:
        HTTPException: If a user with the provided username already exists, returns a 400 BAD REQUEST.

    Returns:
        dict: A JSON response with a success message and the new user's ID.
    """
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use"
        )
    
    hashed = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_passwords=hashed,    
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "User_ID": new_user.id}
