"""
User interface functions for the console todo application.
Handles display and input operations.
"""

from typing import List, Optional, Tuple
from models import Task


def display_menu():
    """Display the main menu options."""
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Complete Status")
    print("6. Exit")
    print("========================")


def display_tasks(tasks: List[Task]):
    """
    Display a formatted list of tasks.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\nNo tasks found.")
        return

    print(f"\n{'ID':<3} {'Status':<8} {'Title':<20} {'Description'}")
    print("-" * 60)

    for task in tasks:
        status_symbol = "✓" if task.completed else "○"
        status_display = f"[{status_symbol}]"
        title_display = task.title[:18] + ".." if len(task.title) > 18 else task.title
        desc_display = task.description[:25] + ".." if len(task.description) > 25 else task.description
        print(f"{task.id:<3} {status_display:<8} {title_display:<20} {desc_display}")


def display_task(task: Task):
    """
    Display a single task with detailed information.

    Args:
        task: Task object to display
    """
    status_symbol = "✓" if task.completed else "○"
    print(f"\nTask #{task.id}: [{status_symbol}] {task.title}")
    print(f"Description: {task.description}")
    print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


def display_error(message: str):
    """
    Display an error message in a formatted way.

    Args:
        message: Error message to display
    """
    print(f"\n❌ Error: {message}")


def display_success(message: str):
    """
    Display a success message in a formatted way.

    Args:
        message: Success message to display
    """
    print(f"\n✅ {message}")


def display_info(message: str):
    """
    Display an informational message in a formatted way.

    Args:
        message: Informational message to display
    """
    print(f"\nℹ️  {message}")


def get_menu_choice() -> Optional[int]:
    """
    Get the user's menu choice.

    Returns:
        The integer choice if valid, None if invalid input
    """
    try:
        choice = input("\nEnter your choice (1-6): ").strip()
        if not choice:
            return None

        choice_int = int(choice)
        if 1 <= choice_int <= 6:
            return choice_int
        return None
    except ValueError:
        return None


def get_task_input() -> Tuple[str, str]:
    """
    Get task input from the user.

    Returns:
        A tuple of (title, description) entered by the user
    """
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()

    description = input("Enter task description (optional, press Enter to skip): ").strip()

    return title, description


def get_task_id(prompt: str = "Enter task ID: ") -> Optional[int]:
    """
    Get a task ID from the user.

    Args:
        prompt: The prompt to display to the user

    Returns:
        The integer ID if valid, None if invalid input
    """
    try:
        task_id_str = input(prompt).strip()
        if not task_id_str:
            return None

        task_id = int(task_id_str)
        if task_id <= 0:
            return None
        return task_id
    except ValueError:
        return None


def get_confirmation(prompt: str = "Are you sure? (y/n): ") -> bool:
    """
    Get confirmation from the user.

    Args:
        prompt: The confirmation prompt to display

    Returns:
        True if user confirms (y/Y), False otherwise
    """
    response = input(prompt).strip().lower()
    return response in ['y', 'yes', 'ye']


# Task ID: T013 - Implement UI display functions in src/ui.py for menu and task listings with status symbols ✓/○
# Task ID: T014 - Implement UI input functions in src/ui.py for getting task title and description