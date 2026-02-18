from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from .models import Task, User # Added User import
from sqlmodel.sql.expression import Select, select
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Synchronous engine for operations
# Configure engine with proper SSL settings for Neon
sync_engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require",
        # Remove channel_binding if it causes issues
        # "channel_binding": "require"  # Commenting out as it might cause connection issues
    } if DATABASE_URL.startswith("postgresql://") else {}
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    with Session(sync_engine) as session:
        yield session

def create_tables():
    """
    Create all tables in the database.
    This should be called when starting the application.
    """
    SQLModel.metadata.create_all(sync_engine)