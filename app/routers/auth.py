from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas import SignupRequest, LoginRequest
from app.models import User         
from app.database import SessionLocal
from app.hashpassword import hash_password, verify_password
from app.database import get_db

#Create a router instance with a prefix for grouping routes
router = APIRouter(prefix="/auth", tags=["auth"])

    
@router.post("/signup")
def signup(signup_data: SignupRequest, db: Session = Depends(get_db)):
    """
    Endpoint to register a new users.
    Expects a JSON body with username and password
    """
    #Check if a user with the given username already exists
    existing_user = db.query(User).filter(User.username == signup_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Username already in use"
        )
    
    # Hash the password and store it in a variable
    hashed = hash_password(signup_data.password)
    

    
    # Create a new user with the hashed password and verification result
    new_user = User(
        username=signup_data.username,
        hashed_passwords=hashed,    
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"message": "User created successfully",
            "User_ID": new_user.id}

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    #check if the username exists
    existing_user = db.query(User).filter(User.username == login_data.username).first()
    if not existing_user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail = "Username not found"
        )
    # Compare the passwords
    stored_hash = existing_user.hashed_passwords
    verify = verify_password(login_data.password, stored_hash)
    assert verify == True, "Problem Verifying Password"
    return{"message": "Login Successful"}