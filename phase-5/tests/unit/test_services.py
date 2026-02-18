"""
Unit tests for the new services in Phase V
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import the services we want to test
from services.recurring_task_service.src.main import calculate_next_occurrence, create_next_recurring_task, Task
from services.notification_service.src.main import send_browser_notification, send_email_notification
from services.audit_service.src.main import log_audit_entry
from services.websocket_service.src.main import ConnectionManager


class TestRecurringTaskService:
    """Test cases for the Recurring Task Service"""

    def test_calculate_next_occurrence_daily(self):
        """Test daily recurrence calculation"""
        due_date = datetime(2026, 1, 15, 10, 0, 0)
        next_date = calculate_next_occurrence(due_date, "daily", 1)

        expected = datetime(2026, 1, 16, 10, 0, 0)
        assert next_date == expected

    def test_calculate_next_occurrence_weekly(self):
        """Test weekly recurrence calculation"""
        due_date = datetime(2026, 1, 15, 10, 0, 0)  # Thursday
        next_date = calculate_next_occurrence(due_date, "weekly", 1)

        expected = datetime(2026, 1, 22, 10, 0, 0)  # Next Thursday
        assert next_date == expected

    def test_calculate_next_occurrence_monthly(self):
        """Test monthly recurrence calculation"""
        due_date = datetime(2026, 1, 15, 10, 0, 0)
        next_date = calculate_next_occurrence(due_date, "monthly", 1)

        expected = datetime(2026, 2, 15, 10, 0, 0)
        assert next_date == expected

    @patch('services.recurring_task_service.src.main.Session')
    @patch('services.recurring_task_service.src.main.select')
    def test_create_next_recurring_task(self, mock_select, mock_session):
        """Test creating the next occurrence of a recurring task"""
        # Create a mock original task
        original_task = Task(
            id=1,
            title="Test Recurring Task",
            description="A recurring task",
            user_id="user123",
            priority="high",
            tags="test,recurring",
            due_date=datetime(2026, 1, 15, 10, 0, 0),
            reminder_time=datetime(2026, 1, 15, 9, 0, 0),
            recurrence_pattern="weekly",
            recurrence_interval=1,
            parent_task_id=None
        )
        
        # Mock the session behavior
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        
        # Mock the select query result
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = original_task
        mock_select_query = MagicMock()
        mock_select_query.where.return_value = mock_select_query
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = original_task
        mock_select.return_value = mock_select_query
        mock_session_instance.exec.return_value = mock_exec_result

        # Call the function
        next_task = create_next_recurring_task(original_task)

        # Verify the new task was created with correct properties
        assert next_task.title == original_task.title
        assert next_task.description == original_task.description
        assert next_task.user_id == original_task.user_id
        assert next_task.priority == original_task.priority
        assert next_task.tags == original_task.tags
        assert next_task.recurrence_pattern == original_task.recurrence_pattern
        assert next_task.recurrence_interval == original_task.recurrence_interval
        assert next_task.parent_task_id == original_task.id  # Should link to original task
        assert next_task.completed is False  # New occurrence should not be completed
        assert next_task.due_date == datetime(2026, 1, 22, 10, 0, 0)  # Next week

        # Verify session methods were called
        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.refresh.assert_called_once()


class TestNotificationService:
    """Test cases for the Notification Service"""

    @patch('services.notification_service.src.main.logger')
    async def test_send_browser_notification(self, mock_logger):
        """Test sending browser notification"""
        user_id = "user123"
        title = "Test Notification"
        message = "This is a test message"

        # Call the function
        await send_browser_notification(user_id, title, message)

        # Verify logging was called
        mock_logger.info.assert_called_once()

    @patch('services.notification_service.src.main.logger')
    async def test_send_email_notification_async(self, mock_logger):
        """Test sending email notification"""
        user_id = "user123"
        recipient_email = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"

        # Call the function
        await send_email_notification(user_id, recipient_email, subject, body)

        # Verify logging was called appropriately
        # Check that the function logged the preparation of the email
        log_calls = [call for call in mock_logger.info.call_args_list if 'Email notification prepared' in str(call)]
        assert len(log_calls) > 0

    @patch('services.notification_service.src.main.send_browser_notification')
    @patch('services.notification_service.src.main.send_email_notification')
    @patch('services.notification_service.src.main.logger')
    async def test_process_reminder_event_with_browser_and_email(self, mock_logger, mock_send_email, mock_send_browser):
        """Test processing a reminder event with both browser and email notifications enabled"""
        event_data = {
            'task_id': 123,
            'user_id': 'user456',
            'title': 'Complete project',
            'due_at': '2026-02-15T10:00:00Z',
            'notification_preferences': {
                'browser_push': True,
                'email': True
            }
        }

        # Call the function
        await process_reminder_event(event_data)

        # Verify that both notification methods were called
        mock_send_browser.assert_called_once()
        mock_send_email.assert_called_once()

        # Verify logging was called
        mock_logger.info.assert_called()


class TestAuditService:
    """Test cases for the Audit Service"""
    
    @patch('services.audit_service.src.main.Session')
    @patch('services.audit_service.src.main.AuditLog')
    def test_log_audit_entry(self, mock_audit_log, mock_session):
        """Test logging an audit entry"""
        event_data = {
            'event_type': 'created',
            'user_id': 'user123',
            'task_id': 123,
            'task_data': {'title': 'Test Task'},
            'timestamp': datetime.utcnow().isoformat(),
            'correlation_id': 'corr123'
        }
        
        # Call the function
        log_audit_entry(event_data)
        
        # Verify the audit log was created and saved
        mock_audit_log.assert_called()
        mock_session.return_value.__enter__.return_value.add.assert_called()
        mock_session.return_value.__enter__.return_value.commit.assert_called()


class TestWebSocketService:
    """Test cases for the WebSocket Service"""
    
    def test_connection_manager(self):
        """Test WebSocket connection manager"""
        manager = ConnectionManager()
        
        # Create mock websocket
        mock_websocket = Mock()
        
        # Test connection
        manager.active_connections.clear()  # Clear any existing connections
        manager.connect(mock_websocket, "user123")
        
        assert len(manager.active_connections["user123"]) == 1
        
        # Test disconnection
        manager.disconnect(mock_websocket, "user123")
        
        assert len(manager.active_connections["user123"]) == 0


if __name__ == "__main__":
    pytest.main([__file__])