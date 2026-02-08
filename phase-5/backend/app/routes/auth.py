from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session  # Removed unused select import
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

from ..database import get_session
from ..auth import create_access_token

# Password hashing context - using pbkdf2 instead of bcrypt to avoid compatibility issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password with pbkdf2
    """
    return pwd_context.hash(password)

# Router for authentication
router = APIRouter(tags=["auth"])

# Request models
class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]

# Mock user storage (in real app, this would be a database)
mock_users_db = {}

@router.post("/auth/signup", response_model=dict)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    # Check if user already exists
    if user_create.email in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_create.password)

    # Create the user (mock)
    user_id = f"user_{len(mock_users_db) + 1}"
    mock_users_db[user_create.email] = {
        "id": user_id,
        "email": user_create.email,
        "hashed_password": hashed_password,
        "name": user_create.name or user_create.email.split("@")[0],
        "created_at": datetime.utcnow()
    }

    # Create access token
    access_token_expires = timedelta(minutes=60 * 24 * 7)  # 7 days
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": user_id,
            "email": user_create.email,
            "name": user_create.name or user_create.email.split("@")[0]
        },
        "token": access_token
    }

@router.post("/auth/signin", response_model=dict)
def signin(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    # Check if user exists
    if user_login.email not in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = mock_users_db[user_login.email]

    # Verify password
    if not pwd_context.verify(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=60 * 24 * 7)  # 7 days
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        },
        "token": access_token
    }

@router.post("/auth/signout", response_model=dict)
def signout():
    """
    Sign out user (currently just returns success).
    """
    return {"success": True}