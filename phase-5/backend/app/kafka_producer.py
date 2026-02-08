"""
Kafka producer module for publishing task events
"""

import json
import asyncio
from datetime import datetime
from kafka import KafkaProducer
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Global producer instance
producer = None


def get_kafka_producer():
    global producer
    if producer is None:
        # Initialize Kafka producer with connection config
        kafka_brokers = "kafka.kafka.svc.cluster.local:9092"  # Default for local dev
        # In production, this would come from environment/config
        producer = KafkaProducer(
            bootstrap_servers=[kafka_brokers],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Ensure message is acknowledged by all replicas
            retries=3,
            linger_ms=5,  # Small delay to batch messages
        )
    return producer


def publish_task_event(task_data: Dict[str, Any], event_type: str):
    """
    Publish a task event to the task-events topic
    """
    try:
        producer_instance = get_kafka_producer()
        
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
        
        # Publish to task-events topic
        producer_instance.send('task-events', value=event_payload)
        producer_instance.flush()  # Ensure message is sent
        
        logger.info(f"Published {event_type} event for task {task_data.get('id')}")
        
    except Exception as e:
        logger.error(f"Failed to publish task event: {str(e)}")
        raise


def publish_reminder_event(task_data: Dict[str, Any]):
    """
    Publish a reminder event to the reminders topic
    """
    try:
        producer_instance = get_kafka_producer()
        
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
        
        # Publish to reminders topic
        producer_instance.send('reminders', value=reminder_payload)
        producer_instance.flush()  # Ensure message is sent
        
        logger.info(f"Published reminder event for task {task_data.get('id')}")
        
    except Exception as e:
        logger.error(f"Failed to publish reminder event: {str(e)}")
        raise


def publish_task_update_event(user_id: str, task_data: Dict[str, Any], action: str):
    """
    Publish a task update event to the task-updates topic for real-time sync
    """
    try:
        producer_instance = get_kafka_producer()
        
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
        
        # Publish to task-updates topic
        producer_instance.send('task-updates', value=update_payload)
        producer_instance.flush()  # Ensure message is sent
        
        logger.info(f"Published task update event for task {task_data.get('id')}")
        
    except Exception as e:
        logger.error(f"Failed to publish task update event: {str(e)}")
        raise