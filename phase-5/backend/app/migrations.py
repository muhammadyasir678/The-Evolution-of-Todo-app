"""
Database migration script for Advanced Cloud Deployment
Adding advanced fields to Task model and supporting models for event-driven architecture.
"""
from sqlmodel import create_engine, SQLModel
from models import Task, Conversation, Message, AuditLog, User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migrations():
    """Run database migrations to create all tables including advanced Task fields."""
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")

    # Create engine
    engine = create_engine(database_url, echo=True)

    # Create all tables (including advanced Task fields and supporting models)
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")
    print("- User table created with email, password, and account metadata")
    print("- Task table created with advanced fields (priority, tags, due_date, etc.)")
    print("- Conversation table created with indexes on user_id")
    print("- Message table created with indexes on user_id and conversation_id")
    print("- AuditLog table created for tracking task operations")

if __name__ == "__main__":
    run_migrations()