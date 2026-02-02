"""
Unit tests for the TaskManager class.
Task ID: T032 - Create tests/test_task_manager.py to test all CRUD operations
Task ID: T033 - Test edge cases: empty list, invalid IDs, duplicate operations
Task ID: T034 - Verify error handling in tests
"""

import pytest
from src.task_manager import TaskManager


def test_initial_state():
    """Test that TaskManager starts with no tasks."""
    tm = TaskManager()
    assert len(tm.get_all_tasks()) == 0


def test_add_task_basic():
    """Test basic task addition."""
    tm = TaskManager()
    task = tm.add_task("Test Task", "Test Description")

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False

    # Check that the task is stored
    all_tasks = tm.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].id == 1


def test_add_multiple_tasks():
    """Test adding multiple tasks."""
    tm = TaskManager()

    task1 = tm.add_task("Task 1", "Description 1")
    task2 = tm.add_task("Task 2", "Description 2")
    task3 = tm.add_task("Task 3", "Description 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3

    all_tasks = tm.get_all_tasks()
    assert len(all_tasks) == 3


def test_get_task():
    """Test getting a specific task."""
    tm = TaskManager()
    added_task = tm.add_task("Test Task", "Test Description")

    retrieved_task = tm.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.title == "Test Task"


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist."""
    tm = TaskManager()

    nonexistent_task = tm.get_task(999)
    assert nonexistent_task is None


def test_get_all_tasks_empty():
    """Test getting all tasks when none exist."""
    tm = TaskManager()
    all_tasks = tm.get_all_tasks()
    assert len(all_tasks) == 0


def test_update_task():
    """Test updating a task."""
    tm = TaskManager()
    original_task = tm.add_task("Original Title", "Original Description")

    success = tm.update_task(1, "Updated Title", "Updated Description")
    assert success is True

    updated_task = tm.get_task(1)
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"


def test_update_task_partial():
    """Test updating only title or description."""
    tm = TaskManager()
    original_task = tm.add_task("Original Title", "Original Description")

    # Update only the title
    success = tm.update_task(1, title="Updated Title")
    assert success is True

    updated_task = tm.get_task(1)
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged

    # Update only the description
    tm.update_task(1, description="New Description")
    updated_task = tm.get_task(1)
    assert updated_task.title == "Updated Title"  # Should remain unchanged
    assert updated_task.description == "New Description"


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist."""
    tm = TaskManager()

    success = tm.update_task(999, "New Title", "New Description")
    assert success is False


def test_delete_task():
    """Test deleting a task."""
    tm = TaskManager()
    tm.add_task("Task to Delete", "Description")

    success = tm.delete_task(1)
    assert success is True

    # Verify the task is gone
    assert tm.get_task(1) is None
    assert len(tm.get_all_tasks()) == 0


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist."""
    tm = TaskManager()

    success = tm.delete_task(999)
    assert success is False


def test_toggle_task_completion():
    """Test toggling task completion status."""
    tm = TaskManager()
    task = tm.add_task("Test Task", "Description")

    # Initially incomplete
    assert task.completed is False

    # Toggle to complete
    success = tm.toggle_task_completion(1)
    assert success is True

    toggled_task = tm.get_task(1)
    assert toggled_task.completed is True

    # Toggle back to incomplete
    success = tm.toggle_task_completion(1)
    assert success is True

    toggled_task = tm.get_task(1)
    assert toggled_task.completed is False


def test_toggle_nonexistent_task():
    """Test toggling completion status of a task that doesn't exist."""
    tm = TaskManager()

    success = tm.toggle_task_completion(999)
    assert success is False


def test_task_validation_on_update():
    """Test that validation is applied when updating tasks."""
    tm = TaskManager()
    tm.add_task("Valid Task", "Valid Description")

    # Try to update with invalid title
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        tm.update_task(1, title="", description="New Description")

    # Try to update with title that's too long
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        tm.update_task(1, title="t" * 201, description="New Description")


def test_invalid_task_ids_handling():
    """Test handling of invalid task IDs in all operations (T026)."""
    tm = TaskManager()
    tm.add_task("Test Task", "Description")

    # Test with negative ID
    assert tm.get_task(-1) is None
    assert tm.update_task(-1, "New Title") is False
    assert tm.delete_task(-1) is False
    assert tm.toggle_task_completion(-1) is False

    # Test with zero ID
    assert tm.get_task(0) is None
    assert tm.update_task(0, "New Title") is False
    assert tm.delete_task(0) is False
    assert tm.toggle_task_completion(0) is False

    # Test with non-integer ID (these should handle gracefully by returning False/None)
    # In Python, type hints don't enforce types at runtime, so we test the behavior
    # Our implementation should handle non-integer inputs gracefully
    # For this, we'll need to modify our implementation to check the type
    assert tm.get_task("invalid") is None
    assert tm.update_task("invalid", "New Title") is False
    assert tm.delete_task("invalid") is False
    assert tm.toggle_task_completion("invalid") is False


def test_edge_cases():
    """Test various edge cases (T030)."""
    tm = TaskManager()

    # Empty task list
    assert len(tm.get_all_tasks()) == 0

    # Get task from empty list
    assert tm.get_task(1) is None

    # Delete from empty list
    assert tm.delete_task(1) is False

    # Toggle in empty list
    assert tm.toggle_task_completion(1) is False