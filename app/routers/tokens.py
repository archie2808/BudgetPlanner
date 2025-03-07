from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import  LoginRequest, Token, TokenData
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

# Load environmnet variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", 15))
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/tokens", tags=["tokens"])

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a JSON Web Token (JWT) with an expiration time.

    This function copies the provided payload data, adds an expiration claim (exp)
    based on the current UTC time and the given time delta, and encodes it using the
    secret key and specified algorithm.

    Args:
        data (dict): The payload data to include in the token, e.g. {"sub": username}.
        expires_delta (timedelta, optional): The time duration for which the token is valid.
            If not provided, a default duration of 15 minutes is used.

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/tokens", response_model=Token)
def create_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }