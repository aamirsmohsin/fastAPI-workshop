# Main Imports
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Database Imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Config Imports
from pydantic_settings import BaseSettings

# Model, Schema
import models, schemas
from schemas import CommentCreate
from typing import List

# Create App
app = FastAPI()

# Database Connection Settings
class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

settings = Settings()

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Establish Database Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Example Routes
@app.get("/")
def main():
    return "Hello, World!"

# Dynamic Parameters - fill in value with a String, don't need the {}
@app.get("/dyanmic/{value}")
def test_dynamic(value):
    return value

# Query Parameters - pass in ?name=<your name> to the end of the route
@app.get("/query")
def test_query(name="World"):
    return f"Hello, {name}!"

# Get Request
@app.get("/deposits/{student_id}", response_model=List[schemas.Deposit])
def get_deposits(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Deposit).filter(models.Deposit.student_id == student_id).all()

# Exercise: Write a Post Request
@app.post("/comments", response_model=schemas.Comment)
def create_comments(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    # 1] Parse the comment parameter
    parsed_comment = models.Comment(student_id=comment.student_id, message=comment.message)

    # 2] Add the comment
    db.add(parsed_comment)

    # 3] Commit the comment
    db.commit()

    # 4] Refresh the database
    db.refresh(parsed_comment)

    # 5] Return a status message
    return parsed_comment

## Additional Notes

# 1] Routers are a way to organize endpoints and group related operations together
# 2] Pass in the expected types for parameters
# 3] Play around with rate-limiting and offset variables
# 4] Review authentication in student-portal