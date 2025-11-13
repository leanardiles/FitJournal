from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Database connection
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Models
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to FitJournal API"}

@app.get("/api/users")
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, user_email, user_first_name FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users

# Run with: uvicorn src.main:app --reload