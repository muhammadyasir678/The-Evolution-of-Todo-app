from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
import uuid

from ..database import get_session
from ..auth import create_access_token
from ..models import User

# Password hashing context - using pbkdf2 instead of bcrypt to avoid compatibility issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password with pbkdf2
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)

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

@router.post("/auth/signup", response_model=dict)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_create.password)

    # Create the user
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=user_create.email,
        hashed_password=hashed_password,
        name=user_create.name or user_create.email.split("@")[0],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=60 * 24 * 7)  # 7 days
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        },
        "token": access_token
    }

@router.post("/auth/signin", response_model=dict)
def signin(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == user_login.email)).first()

    # Check if user exists and password is correct
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update the user's last login time if you have that field
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()

    # Create access token
    access_token_expires = timedelta(minutes=60 * 24 * 7)  # 7 days
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        },
        "token": access_token
    }

@router.post("/auth/signout", response_model=dict)
def signout():
    """
    Sign out user (currently just returns success).
    """
    return {"success": True}