"""
Unit tests for the new services in Phase V
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import the services we want to test
from services.recurring_task_service.src.main import calculate_next_occurrence, create_next_recurring_task
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


class TestNotificationService:
    """Test cases for the Notification Service"""
    
    @patch('services.notification_service.src.main.logger')
    def test_send_browser_notification(self, mock_logger):
        """Test sending browser notification"""
        user_id = "user123"
        title = "Test Notification"
        message = "This is a test message"
        
        # Call the function
        send_browser_notification(user_id, title, message)
        
        # Verify logging was called
        mock_logger.info.assert_called_once()
    
    @patch('services.notification_service.src.main.logger')
    def test_send_email_notification(self, mock_logger):
        """Test sending email notification"""
        user_id = "user123"
        recipient_email = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"
        
        # Call the function
        send_email_notification(user_id, recipient_email, subject, body)
        
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