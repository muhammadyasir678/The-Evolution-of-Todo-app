"""
Unit tests for the Task model and validation functions.
Task ID: T031 - Create tests/test_models.py to test Task validation and creation
Task ID: T033 - Test edge cases: empty list, invalid IDs, duplicate operations
Task ID: T034 - Verify error handling in tests
"""

import pytest
from datetime import datetime
from src.models import Task, validate_task_data


def test_task_creation_valid():
    """Test creating a valid task."""
    task = Task(id=1, title="Test Task", description="Test Description")

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)


def test_task_creation_minimal():
    """Test creating a task with minimal required fields."""
    task = Task(id=1, title="Minimal Task")

    assert task.id == 1
    assert task.title == "Minimal Task"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_defaults():
    """Test that task creation sets proper defaults."""
    task = Task(id=1, title="Default Task")

    assert task.completed is False


def test_task_title_validation():
    """Test validation of task title."""
    # Valid title
    task = Task(id=1, title="Valid Title")
    assert task.title == "Valid Title"

    # Title with whitespace should be stripped
    task_with_spaces = Task(id=1, title="  Spaced Title  ")
    assert task_with_spaces.title == "Spaced Title"


def test_task_title_validation_errors():
    """Test validation errors for task title."""
    # Empty title
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        Task(id=1, title="")

    # Title too long
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        Task(id=1, title="t" * 201)

    # Title with only whitespace
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        Task(id=1, title="   ")

    # Non-string title
    with pytest.raises(ValueError, match="Title must be a string"):
        Task(id=1, title=123)


def test_task_description_validation():
    """Test validation of task description."""
    # Valid description
    task = Task(id=1, title="Test", description="Valid description")
    assert task.description == "Valid description"

    # Long but valid description
    long_desc = "d" * 1000
    task = Task(id=1, title="Test", description=long_desc)
    assert task.description == long_desc


def test_task_description_validation_errors():
    """Test validation errors for task description."""
    # Description too long
    with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
        Task(id=1, title="Test", description="d" * 1001)

    # Non-string description
    with pytest.raises(ValueError, match="Description must be a string"):
        Task(id=1, title="Test", description=123)


def test_validate_task_data():
    """Test the validate_task_data function."""
    # Valid data
    is_valid, errors = validate_task_data("Valid Title", "Valid Description")
    assert is_valid is True
    assert errors == []

    # Valid with empty description
    is_valid, errors = validate_task_data("Valid Title", "")
    assert is_valid is True
    assert errors == []


def test_validate_task_data_invalid_title():
    """Test validation errors for invalid titles."""
    # Empty title
    is_valid, errors = validate_task_data("", "Valid Description")
    assert is_valid is False
    assert "Title must be between 1 and 200 characters" in errors

    # Title too long
    is_valid, errors = validate_task_data("t" * 201, "Valid Description")
    assert is_valid is False
    assert "Title must be between 1 and 200 characters" in errors

    # Title with only whitespace
    is_valid, errors = validate_task_data("   ", "Valid Description")
    assert is_valid is False
    assert "Title must be between 1 and 200 characters" in errors


def test_validate_task_data_invalid_description():
    """Test validation errors for invalid descriptions."""
    # Description too long
    is_valid, errors = validate_task_data("Valid Title", "d" * 1001)
    assert is_valid is False
    assert "Description must be 1000 characters or less" in errors


def test_task_str_representation():
    """Test the string representation of a task."""
    task = Task(id=1, title="Test Task", description="Test Description", completed=True)
    str_repr = str(task)
    assert "1." in str_repr
    assert "[✓]" in str_repr
    assert "Test Task" in str_repr
    assert "Test Description" in str_repr

    # Test incomplete task
    task_incomplete = Task(id=2, title="Incomplete Task", completed=False)
    str_repr = str(task_incomplete)
    assert "[○]" in str_repr