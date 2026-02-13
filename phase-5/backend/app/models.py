from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Enum as saEnum
from typing import Optional
from datetime import datetime
import sqlalchemy as sa

class User(SQLModel, table=True):
    """
    User model representing a registered user with email, password,
    and account metadata.
    """
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """
    Task model representing a user's task with title, description,
    completion status, and timestamps.
    """
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(index=True)  # Foreign key reference to user
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    # Advanced features fields
    priority: Optional[str] = Field(default="medium", sa_column=Column(saEnum("high", "medium", "low", name="priority_enum")))
    tags: Optional[str] = Field(default=None)  # Stored as JSON string
    due_date: Optional[datetime] = Field(default=None)
    reminder_time: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[str] = Field(default=None, sa_column=Column(saEnum("daily", "weekly", "monthly", name="recurrence_enum")))  # daily, weekly, monthly
    recurrence_interval: Optional[int] = Field(default=None)  # e.g., every 2 weeks
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

class Conversation(SQLModel, table=True):
    """
    Conversation model representing a user's chat session with associated metadata.
    """
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(index=True)  # Foreign key reference to user
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Message(SQLModel, table=True):
    """
    Message model representing individual chat exchanges with role (user/assistant),
    content, and timestamp.
    """
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(index=True)  # Foreign key reference to user
    conversation_id: int = Field(index=True)  # Foreign key reference to conversation
    role: str = Field(sa_column=Column(saEnum("user", "assistant", name="message_role"), nullable=False))
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class AuditLog(SQLModel, table=True):
    """
    AuditLog model for tracking all task operations.
    """
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(index=True)  # Reference to user
    task_id: Optional[int] = Field(default=None, index=True)  # Reference to task
    action: str = Field(sa_column=Column(saEnum("created", "updated", "deleted", "completed", name="action_enum")))  # Action performed
    details: Optional[str] = Field(default=None)  # JSONB field for task data or changes
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of the event
    correlation_id: Optional[str] = Field(default=None)  # For tracking related events in event flows

class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    priority: Optional[str] = Field(default="medium", sa_column=Column(saEnum("high", "medium", "low", name="priority_enum")))
    tags: Optional[str] = Field(default=None)  # Stored as JSON string
    due_date: Optional[datetime] = Field(default=None)
    reminder_time: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[str] = Field(default=None, sa_column=Column(saEnum("daily", "weekly", "monthly", name="recurrence_enum")))  # daily, weekly, monthly
    recurrence_interval: Optional[int] = Field(default=None)  # e.g., every 2 weeks
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, sa_column=Column(saEnum("high", "medium", "low", name="priority_enum")))
    tags: Optional[str] = Field(default=None)  # Stored as JSON string
    due_date: Optional[datetime] = Field(default=None)
    reminder_time: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[str] = Field(default=None, sa_column=Column(saEnum("daily", "weekly", "monthly", name="recurrence_enum")))  # daily, weekly, monthly
    recurrence_interval: Optional[int] = Field(default=None)  # e.g., every 2 weeks
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

class TaskPublic(TaskBase):
    """
    Public schema for task representation in API responses.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    parent_task_id: Optional[int] = None