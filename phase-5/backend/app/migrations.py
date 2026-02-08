"""
Database migration script for AI-Powered Todo Chatbot - Task T013
Adding Conversation and Message models to support chat functionality.
"""
from sqlmodel import create_engine, SQLModel
from .models import Conversation, Message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migrations():
    """Run database migrations to create Conversation and Message tables."""
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")

    # Create engine
    engine = create_engine(database_url, echo=True)

    # Create all tables (including new Conversation and Message tables)
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")
    print("- Conversation table created with indexes on user_id")
    print("- Message table created with indexes on user_id and conversation_id")

if __name__ == "__main__":
    run_migrations()