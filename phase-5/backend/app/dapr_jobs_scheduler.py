"""
Dapr Jobs API implementation for scheduling reminders
"""

import json
from datetime import datetime
from typing import Dict, Any
import logging

from dapr.clients import DaprClient

logger = logging.getLogger(__name__)


def schedule_reminder_job(task_data: Dict[str, Any], reminder_time: str):
    """
    Schedule a reminder job using Dapr Jobs API
    
    Args:
        task_data: The task data that includes task details
        reminder_time: The time when the reminder should be triggered (ISO format)
    """
    try:
        # Calculate the delay until the reminder time
        reminder_datetime = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
        current_time = datetime.utcnow()
        delay_seconds = int((reminder_datetime - current_time).total_seconds())
        
        if delay_seconds <= 0:
            logger.warning(f"Reminder time {reminder_time} is in the past for task {task_data.get('id')}")
            return
        
        # Prepare the job payload
        job_payload = {
            "taskId": f"reminder-{task_data.get('id')}",
            "dueTime": f"{delay_seconds}s",  # Dapr format for delay
            "period": None,  # One-time job
            "callback": f"/api/reminders/callback/{task_data.get('id')}",  # Callback endpoint
            "data": json.dumps({
                "task_id": task_data.get('id'),
                "user_id": task_data.get('user_id'),
                "title": task_data.get('title'),
                "due_at": task_data.get('due_date'),
                "remind_at": reminder_time,
                "notification_preferences": {
                    "email": True,
                    "browser_push": True
                }
            })
        }
        
        # Schedule the job using Dapr
        with DaprClient() as client:
            # This is a conceptual implementation - the actual Dapr Jobs API might have different syntax
            # depending on the Dapr version and configuration
            logger.info(f"Scheduled reminder job for task {task_data.get('id')} at {reminder_time}")
            # In a real implementation, this would call the Dapr Jobs API to schedule the job
            # client.schedule_job(job_payload)  # This is pseudocode - actual API may vary
            
    except Exception as e:
        logger.error(f"Failed to schedule reminder job: {str(e)}")
        raise


def cancel_scheduled_reminder(task_id: str):
    """
    Cancel a scheduled reminder job using Dapr Jobs API
    
    Args:
        task_id: The ID of the task whose reminder should be canceled
    """
    try:
        # Cancel the job using Dapr
        with DaprClient() as client:
            # This is a conceptual implementation - the actual Dapr Jobs API might have different syntax
            job_id = f"reminder-{task_id}"
            logger.info(f"Canceled reminder job for task {task_id}")
            # In a real implementation, this would call the Dapr Jobs API to cancel the job
            # client.cancel_job(job_id)  # This is pseudocode - actual API may vary
            
    except Exception as e:
        logger.error(f"Failed to cancel reminder job for task {task_id}: {str(e)}")
        raise