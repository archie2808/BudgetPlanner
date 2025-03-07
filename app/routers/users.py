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
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError




router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(signup_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user resource.

    This endpoint replaces the old /signup. It checks for an existing username, hashes the
    password, and creates a new user.
    """
    existing_user = db.query(User).filter(User.username == signup_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use"
        )
    
    hashed = hash_password(signup_data.password)
    new_user = User(
        username=signup_data.username,
        hashed_passwords=hashed,  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}