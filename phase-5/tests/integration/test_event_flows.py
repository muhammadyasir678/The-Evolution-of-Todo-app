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


if __name__ == "__main__":
    pytest.main([__file__])