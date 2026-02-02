"""
Utility functions for input validation and processing.
"""

import re
from typing import Optional


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate a task title.

    Args:
        title: The title to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not isinstance(title, str):
        return False, "Title must be a string"

    stripped_title = title.strip()
    if len(stripped_title) < 1 or len(stripped_title) > 200:
        return False, "Title must be between 1 and 200 characters"

    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate a task description.

    Args:
        description: The description to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not isinstance(description, str):
        return False, "Description must be a string"

    if len(description) > 1000:
        return False, "Description must be 1000 characters or less"

    return True, ""


def validate_task_id(task_id_str: str) -> Optional[int]:
    """
    Validate and convert a task ID string to an integer.

    Args:
        task_id_str: The string representation of a task ID

    Returns:
        The integer ID if valid, None otherwise
    """
    if not isinstance(task_id_str, str):
        return None

    try:
        task_id = int(task_id_str.strip())
        # Task IDs must be positive integers
        if task_id <= 0:
            return None
        return task_id
    except ValueError:
        return None


def validate_menu_choice(choice_str: str) -> Optional[int]:
    """
    Validate and convert a menu choice string to an integer.

    Args:
        choice_str: The string representation of a menu choice

    Returns:
        The integer choice if valid (1-6), None otherwise
    """
    if not isinstance(choice_str, str):
        return None

    try:
        choice = int(choice_str.strip())
        # Menu choices are typically 1-6
        if choice < 1 or choice > 6:
            return None
        return choice
    except ValueError:
        return None


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by stripping leading/trailing whitespace.

    Args:
        input_str: The input string to sanitize

    Returns:
        The sanitized string
    """
    if not isinstance(input_str, str):
        return ""
    return input_str.strip()