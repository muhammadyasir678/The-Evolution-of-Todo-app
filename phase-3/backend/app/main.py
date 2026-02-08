from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks
from .routes import auth
from .routes import chat
from .database import create_tables
import os

# Create the FastAPI app
app = FastAPI(title="Todo App API", version="1.0.0")

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js default port
    "http://localhost:3001",  # Alternative Next.js port
    "http://127.0.0.1:3000",  # Alternative localhost
    "http://127.0.0.1:3001",  # Alternative localhost
    "https://the-evolution-of-todo-app-mu.vercel.app",  # Deployed frontend
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional headers that might be needed
    allow_origin_regex=r"https://the-evolution-of-todo-app-mu.vercel.app",  # For Vercel deployments
)

# Include the auth, task, and chat routes
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

@app.on_event("startup")
def on_startup():
    """
    Startup event handler to create database tables.
    """
    create_tables()

@app.get("/")
def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Todo App API is running"}

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "API is running correctly"}