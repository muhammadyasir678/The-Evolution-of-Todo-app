from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Enum as saEnum
from typing import Optional
from datetime import datetime
import sqlalchemy as sa

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

class ConversationCreate(SQLModel):
    """
    Schema for creating a new conversation.
    """
    user_id: str

class ConversationPublic(SQLModel):
    """
    Public schema for conversation representation in API responses.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(SQLModel):
    """
    Schema for creating a new message.
    """
    user_id: str
    conversation_id: int
    role: str
    content: str

class MessagePublic(SQLModel):
    """
    Public schema for message representation in API responses.
    """
    id: int
    user_id: str
    conversation_id: int
    role: str
    content: str
    created_at: datetime

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
    pass

class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class TaskPublic(TaskBase):
    """
    Public schema for task representation in API responses.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime