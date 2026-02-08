"""
Dapr-based Kafka producer module for publishing task events
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any
import logging

from dapr.clients import DaprClient

logger = logging.getLogger(__name__)


def publish_task_event(task_data: Dict[str, Any], event_type: str):
    """
    Publish a task event to the task-events topic via Dapr
    """
    try:
        with DaprClient() as client:
            event_payload = {
                "event_id": task_data.get('id'),  # Using task ID as event ID for simplicity
                "event_type": event_type,
                "task_id": task_data.get('id'),
                "user_id": task_data.get('user_id'),
                "task_data": task_data,
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": task_data.get('correlation_id', ''),
                "source_service": "backend-api"
            }
            
            # Publish to task-events topic via Dapr pubsub
            client.publish_event(
                pubsub_name='kafka-pubsub',
                topic_name='task-events',
                data=json.dumps(event_payload),
                data_content_type='application/json'
            )
            
            logger.info(f"Published {event_type} event for task {task_data.get('id')} via Dapr")
        
    except Exception as e:
        logger.error(f"Failed to publish task event via Dapr: {str(e)}")
        raise


def publish_reminder_event(task_data: Dict[str, Any]):
    """
    Publish a reminder event to the reminders topic via Dapr
    """
    try:
        with DaprClient() as client:
            reminder_payload = {
                "event_id": f"reminder-{task_data.get('id')}",
                "task_id": task_data.get('id'),
                "user_id": task_data.get('user_id'),
                "title": task_data.get('title'),
                "due_at": task_data.get('due_date'),
                "remind_at": task_data.get('reminder_time'),
                "notification_preferences": {
                    "email": True,
                    "browser_push": True
                },
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": task_data.get('correlation_id', '')
            }
            
            # Publish to reminders topic via Dapr pubsub
            client.publish_event(
                pubsub_name='kafka-pubsub',
                topic_name='reminders',
                data=json.dumps(reminder_payload),
                data_content_type='application/json'
            )
            
            logger.info(f"Published reminder event for task {task_data.get('id')} via Dapr")
        
    except Exception as e:
        logger.error(f"Failed to publish reminder event via Dapr: {str(e)}")
        raise


def publish_task_update_event(user_id: str, task_data: Dict[str, Any], action: str):
    """
    Publish a task update event to the task-updates topic via Dapr for real-time sync
    """
    try:
        with DaprClient() as client:
            update_payload = {
                "event_id": f"update-{task_data.get('id')}-{datetime.utcnow().timestamp()}",
                "user_id": user_id,
                "task_id": task_data.get('id'),
                "action": action,
                "task_data": {
                    "id": task_data.get('id'),
                    "title": task_data.get('title'),
                    "completed": task_data.get('completed', False),
                    "priority": task_data.get('priority', 'medium'),
                    "due_date": task_data.get('due_date'),
                },
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": task_data.get('correlation_id', ''),
                "source_service": "backend-api"
            }
            
            # Publish to task-updates topic via Dapr pubsub
            client.publish_event(
                pubsub_name='kafka-pubsub',
                topic_name='task-updates',
                data=json.dumps(update_payload),
                data_content_type='application/json'
            )
            
            logger.info(f"Published task update event for task {task_data.get('id')} via Dapr")
        
    except Exception as e:
        logger.error(f"Failed to publish task update event via Dapr: {str(e)}")
        raise