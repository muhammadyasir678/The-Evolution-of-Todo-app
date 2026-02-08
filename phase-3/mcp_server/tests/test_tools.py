"""
Test suite for MCP tools - Task T080
Tests for add_task, list_tasks, complete_task, delete_task, update_task
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest
)
from sqlmodel import Session, select
from backend.app.models import Task


@pytest.mark.asyncio
async def test_add_task_success():
    """Test T085: add_task creates task in database with proper user isolation"""
    request = AddTaskRequest(
        user_id="user-123",
        title="Test task",
        description="Test description"
    )

    with patch('src.tools.engine') as mock_engine:
        mock_session = Mock(spec=Session)
        mock_task = Mock()
        mock_task.id = 1
        mock_task.title = "Test task"

        # Mock the session context manager behavior
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)

        # Mock the add, commit, refresh operations
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Mock returning the created task
        mock_session.exec.return_value.first.return_value = mock_task
        mock_session.exec.return_value.scalar.return_value = 1

        with patch('src.tools.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.__enter__ = Mock(return_value=mock_session)
            mock_session_instance.__exit__ = Mock(return_value=None)
            mock_session_class.return_value = mock_session_instance

            result = await add_task(request)

            assert result["success"] is True
            assert result["task_id"] == 1
            assert "created successfully" in result["message"]

            # Verify session operations were called
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_list_tasks_success():
    """Test T086: list_tasks returns user-specific tasks with status filtering"""
    request = ListTasksRequest(
        user_id="user-123",
        status="all"
    )

    with patch('src.tools.engine'):
        mock_task = Mock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_task.description = "Test description"
        mock_task.completed = False
        mock_task.created_at = "2023-01-01T00:00:00"

        mock_session = Mock(spec=Session)
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_session.exec.return_value.all.return_value = [mock_task]

        with patch('src.tools.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.__enter__ = Mock(return_value=mock_session)
            mock_session_instance.__exit__ = Mock(return_value=None)
            mock_session_class.return_value = mock_session_instance

            result = await list_tasks(request)

            assert result["success"] is True
            assert result["count"] == 1
            assert len(result["tasks"]) == 1
            assert result["tasks"][0]["id"] == 1


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test T087: complete_task toggles status and respects user isolation"""
    request = CompleteTaskRequest(
        user_id="user-123",
        task_id=1
    )

    with patch('src.tools.engine'):
        mock_task = Mock()
        mock_task.id = 1
        mock_task.title = "Test task"
        mock_task.completed = True

        mock_session = Mock(spec=Session)
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_session.exec.return_value.first.return_value = mock_task

        with patch('src.tools.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.__enter__ = Mock(return_value=mock_session)
            mock_session_instance.__exit__ = Mock(return_value=None)
            mock_session_class.return_value = mock_session_instance

            result = await complete_task(request)

            assert result["success"] is True
            assert result["task_id"] == 1
            assert result["completed"] is True


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test T088: delete_task removes task and respects user isolation"""
    request = DeleteTaskRequest(
        user_id="user-123",
        task_id=1
    )

    with patch('src.tools.engine'):
        mock_task = Mock()
        mock_task.id = 1
        mock_task.title = "Test task"

        mock_session = Mock(spec=Session)
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_session.exec.return_value.first.return_value = mock_task

        with patch('src.tools.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.__enter__ = Mock(return_value=mock_session)
            mock_session_instance.__exit__ = Mock(return_value=None)
            mock_session_class.return_value = mock_session_instance

            result = await delete_task(request)

            assert result["success"] is True
            assert result["task_id"] == 1
            # Verify delete was called
            mock_session.delete.assert_called_once_with(mock_task)


@pytest.mark.asyncio
async def test_update_task_success():
    """Test T089: update_task modifies task and respects user isolation"""
    request = UpdateTaskRequest(
        user_id="user-123",
        task_id=1,
        title="Updated task",
        description="Updated description"
    )

    with patch('src.tools.engine'):
        mock_task = Mock()
        mock_task.id = 1
        mock_task.title = "Updated task"
        mock_task.description = "Updated description"

        mock_session = Mock(spec=Session)
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_session.exec.return_value.first.return_value = mock_task

        with patch('src.tools.Session') as mock_session_class:
            mock_session_instance = Mock()
            mock_session_instance.__enter__ = Mock(return_value=mock_session)
            mock_session_instance.__exit__ = Mock(return_value=None)
            mock_session_class.return_value = mock_session_instance

            result = await update_task(request)

            assert result["success"] is True
            assert result["task_id"] == 1
            assert result["title"] == "Updated task"
            assert result["description"] == "Updated description"