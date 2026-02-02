"""
TaskManager class for handling task operations.
Implements CRUD operations for tasks with in-memory storage.
"""

from typing import Dict, List, Optional, Union, Any
from models import Task, validate_task_data


class TaskManager:
    """
    Manages tasks in memory using a dictionary for storage.

    Task ID: T010 - Implement TaskManager class in src/task_manager.py with tasks dict and next_id counter
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task dictionary and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the given title and description.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The created Task object

        Raises:
            ValueError: If the title is invalid
        """
        # Validate input data
        is_valid, errors = validate_task_data(title, description)
        if not is_valid:
            raise ValueError("; ".join(errors))

        # Create a new task with the next available ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False  # Default to incomplete
        )

        # Add task to storage
        self._tasks[self._next_id] = task

        # Increment the ID counter for the next task
        self._next_id += 1

        return task

    def get_task(self, task_id: Union[int, Any]) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        # Task ID: T026 - Add validation in all TaskManager methods to handle invalid task IDs gracefully
        if not isinstance(task_id, int) or task_id <= 0:
            return None
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            A list of all Task objects, sorted by ID
        """
        return sorted(list(self._tasks.values()), key=lambda task: task.id)

    def update_task(self, task_id: Union[int, Any], title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the task was updated, False if the task was not found
        """
        # Task ID: T026 - Add validation in all TaskManager methods to handle invalid task IDs gracefully
        if not isinstance(task_id, int) or task_id <= 0:
            return False

        # Check if the task exists
        if task_id not in self._tasks:
            return False

        # Get the current task
        current_task = self._tasks[task_id]

        # Prepare the new title and description
        new_title = title if title is not None else current_task.title
        new_description = description if description is not None else current_task.description

        # Validate the new data
        is_valid, errors = validate_task_data(new_title, new_description)
        if not is_valid:
            raise ValueError("; ".join(errors))

        # Update the task
        self._tasks[task_id] = Task(
            id=current_task.id,
            title=new_title,
            description=new_description,
            completed=current_task.completed,
            created_at=current_task.created_at
        )

        return True

    def delete_task(self, task_id: Union[int, Any]) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if the task was not found
        """
        # Task ID: T026 - Add validation in all TaskManager methods to handle invalid task IDs gracefully
        if not isinstance(task_id, int) or task_id <= 0:
            return False

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: Union[int, Any]) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if the task was not found
        """
        # Task ID: T026 - Add validation in all TaskManager methods to handle invalid task IDs gracefully
        if not isinstance(task_id, int) or task_id <= 0:
            return False

        if task_id in self._tasks:
            current_task = self._tasks[task_id]
            # Create a new task with toggled completion status
            self._tasks[task_id] = Task(
                id=current_task.id,
                title=current_task.title,
                description=current_task.description,
                completed=not current_task.completed,
                created_at=current_task.created_at
            )
            return True
        return False


# Task ID: T026 - Add validation in all TaskManager methods to handle invalid task IDs gracefully
# This is implemented in each method by checking if the task_id exists before operating on it