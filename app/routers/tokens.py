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
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError

# Load environmnet variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", 15))
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens")

router = APIRouter(prefix="/tokens", tags=["tokens"])

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a JWT with an expiration time.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    """
    Function to retrieve and validate the current user based on the JWT token.
    Provided all checks pass, user object can be passed on in the program for other authentication
    """
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNATHORISED,
        detail = "Could not validate credentials.",
        headers ={"WWW-Authenticate": "bearer"}    
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, alogrithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None: 
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    # Retrieve the user from the database based on the username from the token
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate the user and create a token resource.

    This endpoint (formerly /login) verifies credentials and returns a JWT.
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