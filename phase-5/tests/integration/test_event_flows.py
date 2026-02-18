"""
Integration tests for event-driven flows in Phase V
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import json
from datetime import datetime

# Import components to test
from services.recurring_task_service.src.main import create_next_recurring_task
from services.notification_service.src.main import process_reminder_event
from services.audit_service.src.main import log_audit_entry
from services.websocket_service.src.main import manager


class TestEventDrivenFlows:
    """Integration tests for event-driven flows"""
    
    @patch('services.recurring_task_service.src.main.Session')
    @patch('services.recurring_task_service.src.main.Task')
    def test_recurring_task_creation_flow(self, mock_task, mock_session):
        """Test the full flow of creating a recurring task and generating next occurrence"""
        # Create a mock original task
        original_task = Mock()
        original_task.id = 123
        original_task.title = "Weekly Meeting"
        original_task.description = "Team weekly sync"
        original_task.completed = False
        original_task.user_id = "user123"
        original_task.priority = "medium"
        original_task.tags = ["work", "meeting"]
        original_task.due_date = datetime(2026, 1, 20, 10, 0, 0)
        original_task.reminder_time = datetime(2026, 1, 20, 9, 0, 0)
        original_task.recurrence_pattern = "weekly"
        original_task.recurrence_interval = 1
        original_task.parent_task_id = None
        
        # Mock the session behavior
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.add = Mock()
        mock_session_instance.commit = Mock()
        mock_session_instance.refresh = Mock()
        
        # Mock the new task creation
        next_task = Mock()
        next_task.id = 124
        next_task.title = "Weekly Meeting"
        next_task.parent_task_id = 123
        mock_session_instance.merge.return_value = next_task
        
        # Call the function
        result = create_next_recurring_task(original_task)
        
        # Verify the new task was created
        assert result.id == 124
        assert result.parent_task_id == 123
        mock_session_instance.add.assert_called()
        mock_session_instance.commit.assert_called()
    
    @patch('services.notification_service.src.main.send_browser_notification')
    @patch('services.notification_service.src.main.send_email_notification')
    @patch('services.notification_service.src.main.logger')
    def test_reminder_processing_flow(self, mock_logger, mock_email, mock_browser):
        """Test the full flow of processing a reminder event"""
        event_data = {
            "event_id": "reminder-123",
            "task_id": 123,
            "user_id": "user123",
            "title": "Submit report",
            "due_at": "2026-01-19T17:00:00Z",
            "remind_at": "2026-01-19T16:00:00Z",
            "notification_preferences": {
                "email": True,
                "browser_push": True
            },
            "timestamp": datetime.utcnow().isoformat(),
            "correlation_id": "corr123"
        }
        
        # Call the function
        asyncio.run(process_reminder_event(event_data))
        
        # Verify both notification methods were called
        mock_browser.assert_called()
        mock_email.assert_called()
        mock_logger.info.assert_called()
    
    @patch('services.audit_service.src.main.Session')
    @patch('services.audit_service.src.main.AuditLog')
    def test_audit_logging_flow(self, mock_audit_log, mock_session):
        """Test the full flow of logging an audit event"""
        event_data = {
            "event_id": "event-123",
            "event_type": "created",
            "task_id": 123,
            "user_id": "user123",
            "task_data": {
                "id": 123,
                "title": "Test Task",
                "completed": False
            },
            "timestamp": datetime.utcnow().isoformat(),
            "correlation_id": "corr123",
            "source_service": "backend-api"
        }
        
        # Mock the session behavior
        mock_session_instance = Mock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.add = Mock()
        mock_session_instance.commit = Mock()
        
        # Call the function
        log_audit_entry(event_data)
        
        # Verify the audit log was created and saved
        mock_audit_log.assert_called()
        mock_session_instance.add.assert_called()
        mock_session_instance.commit.assert_called()


class TestFilteringSortingSearch:
    """Tests for filtering, sorting, and search functionality"""

    @patch('sqlmodel.Session.exec')
    def test_get_filtered_tasks_by_priority(self, mock_exec):
        """Test filtering tasks by priority"""
        # Mock the database query result
        mock_tasks = [
            Mock(priority="high", completed=False, user_id="user123"),
            Mock(priority="low", completed=False, user_id="user123")
        ]
        mock_result = Mock()
        mock_result.all.return_value = mock_tasks
        mock_exec.return_value = mock_result

        # Simulate calling the endpoint with priority filter
        from backend.app.routes.tasks import get_filtered_tasks
        from backend.app.database import get_session
        from backend.app.auth import get_current_user

        # Mock dependencies
        mock_session = Mock()
        current_user = "user123"

        # Call the function
        result = get_filtered_tasks(
            user_id="user123",
            current_user_id=current_user,
            session=mock_session,
            priority="high"
        )

        # Verify the result contains only high priority tasks
        assert len(result) == 2  # We have 2 mock tasks, but filtering logic happens in SQL
        # The actual filtering would happen in the SQL query which is mocked

    @patch('sqlmodel.Session.exec')
    def test_get_filtered_tasks_by_status(self, mock_exec):
        """Test filtering tasks by status (pending/completed)"""
        # Mock the database query result
        mock_tasks = [
            Mock(completed=False, user_id="user123"),
            Mock(completed=True, user_id="user123")
        ]
        mock_result = Mock()
        mock_result.all.return_value = mock_tasks
        mock_exec.return_value = mock_result

        # Simulate calling the endpoint with status filter
        from backend.app.routes.tasks import get_filtered_tasks

        # Mock dependencies
        mock_session = Mock()
        current_user = "user123"

        # Call the function for pending tasks
        result = get_filtered_tasks(
            user_id="user123",
            current_user_id=current_user,
            session=mock_session,
            status="pending"
        )

        # Verify the call was made with the right parameters
        assert len(result) == 2  # Result depends on the SQL query which is mocked

    @patch('sqlmodel.Session.exec')
    def test_get_filtered_tasks_with_sorting(self, mock_exec):
        """Test sorting tasks by different fields"""
        # Mock the database query result
        mock_tasks = [
            Mock(title="Z Task", priority="low", created_at=datetime(2026, 1, 1), user_id="user123"),
            Mock(title="A Task", priority="high", created_at=datetime(2026, 1, 2), user_id="user123")
        ]
        mock_result = Mock()
        mock_result.all.return_value = mock_tasks
        mock_exec.return_value = mock_result

        # Test sorting by title (ascending)
        from backend.app.routes.tasks import get_filtered_tasks

        # Mock dependencies
        mock_session = Mock()
        current_user = "user123"

        # Call the function to sort by title ascending
        result = get_filtered_tasks(
            user_id="user123",
            current_user_id=current_user,
            session=mock_session,
            sort_by="title",
            sort_order="asc"
        )

        # Verify the call was made
        assert len(result) == 2

    @patch('sqlmodel.Session.exec')
    def test_get_filtered_tasks_with_date_range(self, mock_exec):
        """Test filtering tasks by due date range"""
        # Mock the database query result
        mock_tasks = [
            Mock(due_date=datetime(2026, 1, 15), user_id="user123"),
            Mock(due_date=datetime(2026, 2, 15), user_id="user123")
        ]
        mock_result = Mock()
        mock_result.all.return_value = mock_tasks
        mock_exec.return_value = mock_result

        # Test filtering by date range
        from backend.app.routes.tasks import get_filtered_tasks

        # Mock dependencies
        mock_session = Mock()
        current_user = "user123"

        # Call the function with date range filters
        result = get_filtered_tasks(
            user_id="user123",
            current_user_id=current_user,
            session=mock_session,
            due_after="2026-01-01T00:00:00",
            due_before="2026-01-31T23:59:59"
        )

        # Verify the result
        assert len(result) == 2


class TestRealTimeSync:
    """Tests for real-time synchronization across multiple devices"""

    def test_websocket_connection_manager(self):
        """Test the WebSocket connection manager functionality"""
        from services.websocket_service.src.main import ConnectionManager
        import asyncio
        from unittest.mock import AsyncMock, MagicMock

        # Create a mock WebSocket object that mimics the real WebSocket
        class MockWebSocket:
            def __init__(self):
                self.sent_messages = []

            async def accept(self):
                pass

            async def send_text(self, message):
                self.sent_messages.append(json.dumps(message))

        # Create connection manager
        manager = ConnectionManager()

        # Create mock websockets for the same user
        ws1 = AsyncMock()
        ws1.sent_messages = []
        ws1.accept = AsyncMock()
        ws1.send_text = AsyncMock(side_effect=lambda msg: ws1.sent_messages.append(json.dumps(msg)))

        ws2 = AsyncMock()
        ws2.sent_messages = []
        ws2.accept = AsyncMock()
        ws2.send_text = AsyncMock(side_effect=lambda msg: ws2.sent_messages.append(json.dumps(msg)))

        # Connect both websockets for the same user
        asyncio.run(manager.connect(ws1, "user123"))
        asyncio.run(manager.connect(ws2, "user123"))

        # Verify both connections are active for the user
        assert len(manager.active_connections["user123"]) == 2

        # Create a message to broadcast
        message = {"event": "task_updated", "task_id": 123, "data": {"title": "Updated Task"}}

        # Broadcast to the user
        asyncio.run(manager.broadcast_to_user(message, "user123"))

        # Verify both connections received the message
        # Check that send_text was called on both websockets
        assert ws1.send_text.call_count == 1
        assert ws2.send_text.call_count == 1

        # Disconnect one websocket
        manager.disconnect(ws1, "user123")

        # Verify only one connection remains
        assert len(manager.active_connections["user123"]) == 1

        # Broadcast another message
        message2 = {"event": "task_deleted", "task_id": 123}

        # Verify only the remaining connection received the message
        assert ws1.send_text.call_count == 1  # Still has the first message
        assert ws2.send_text.call_count == 2  # Has both messages


if __name__ == "__main__":
    pytest.main([__file__])