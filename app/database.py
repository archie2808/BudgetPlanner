from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/budgetdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependency function to get a database session
def get_db():
    db = SessionLocal() #Create a new db session
    try:
        yield db
    finally:
        db.close() #Make sure the session is closed after the request