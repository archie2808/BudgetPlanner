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

# Load environmnet variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES")
ALGORITHM = os.getenv("ALGORITHM")

#Create a router instance with a prefix for grouping routes
router = APIRouter(prefix="/auth", tags=["auth"])

    

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

@router.post("/signup")
def signup(signup_data: SignupRequest, db: Session = Depends(get_db)):
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

    return {"message": "User created successfully", "User_ID": new_user.id}

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide a JWT access token.

    This endpoint verifies the user's credentials by:
      1. Retrieving the user record from the database using the provided username.
      2. Comparing the provided password with the stored hashed password.
      3. Generating a JWT token that contains the user's username as a subject claim ("sub") 
         if the credentials are valid.

    Args:
        login_data (LoginRequest): A Pydantic model containing login data (username and password).
        db (Session, optional): A SQLAlchemy session provided by the dependency injection.

    Raises:
        HTTPException: 
            - If the user is not found, returns a 400 BAD REQUEST with "Username not found".
            - If the password verification fails, returns a 400 BAD REQUEST with "Incorrect password".

    Returns:
        dict: A JSON response containing the generated JWT access token and its type ("bearer").
    """
    existing_user = db.query(User).filter(User.username == login_data.username).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found"
        )
    
    stored_hash = existing_user.hashed_passwords
    if not verify_password(login_data.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existing_user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}