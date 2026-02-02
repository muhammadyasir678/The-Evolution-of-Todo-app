'''
Task model for the console todo application.
Represents a single todo task with id, title, description, completion status, and creation timestamp.
'''

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union, Any


@dataclass
class Task:
    """
    Represents a single todo task.

    Task model for the console todo application.
    Task ID: T007 - Implement Task model in src/models.py with id, title, description, completed, created_at
    Task ID: T008 - Implement Task validation in src/models.py for title (1-200 chars) and description (max 1000 chars)
    """
    id: int
    title: Union[str, Any]  # Accept any type so validation can catch non-strings
    description: Union[str, Any] = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task attributes after initialization."""
        # Validate title
        if not isinstance(self.title, str):
            raise ValueError("Title must be a string")

        # Strip whitespace for validation
        stripped_title = self.title.strip()
        if len(stripped_title) < 1 or len(stripped_title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")

        # Update title to stripped version
        self.title = stripped_title

        # Validate description
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

        if len(self.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

    def __str__(self) -> str:
        """Return a formatted string representation of the task."""
        status_symbol = "✓" if self.completed else "○"
        return f"{self.id}. [{status_symbol}] {self.title} - {self.description}"


def validate_task_data(title: str, description: str = "") -> tuple[bool, list[str]]:
    """
    Validate task data before creation or update.

    Args:
        title: The task title to validate
        description: The task description to validate

    Returns:
        A tuple of (is_valid, list_of_error_messages)
    """
    errors = []

    # Validate title
    if not isinstance(title, str):
        errors.append("Title must be a string")
    elif len(title.strip()) < 1 or len(title.strip()) > 200:
        errors.append("Title must be between 1 and 200 characters")

    # Validate description
    if not isinstance(description, str):
        errors.append("Description must be a string")
    elif len(description) > 1000:
        errors.append("Description must be 1000 characters or less")

    return len(errors) == 0, errors