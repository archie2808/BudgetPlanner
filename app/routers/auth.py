from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas import SignupRequest  
from app.models import User         
from app.database import SessionLocal
from app.hashpassword import hash_password, verify_password

#Create a router instance with a prefix for grouping routes
router = APIRouter(prefix="/auth", tags=["auth"])

#Dependency function to get a database session
def get_db():
    db = SessionLocal() #Create a new db session
    try:
        yield db
    finally:
        db.close() #Make sure the session is closed after the request
    
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