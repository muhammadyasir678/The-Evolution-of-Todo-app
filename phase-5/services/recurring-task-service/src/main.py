"""
Recurring Task Service
This service consumes task-events from Kafka and handles recurring task logic.
When a recurring task is completed, it creates the next occurrence based on the recurrence pattern.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI
from kafka import KafkaConsumer
from sqlmodel import Session, select

from backend.app.database import engine
from backend.app.models import Task

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Recurring Task Service")

# Initialize Dapr extension
dapr_app = DaprApp(app)

# Kafka consumer configuration
KAFKA_BROKERS = "kafka.kafka.svc.cluster.local:9092"
TASK_EVENTS_TOPIC = "task-events"


@app.on_event("startup")
async def startup_event():
    """Initialize the Kafka consumer and start listening for events."""
    logger.info("Starting Recurring Task Service...")
    # Start the Kafka consumer in a background task
    asyncio.create_task(consume_task_events())


def calculate_next_occurrence(due_date: datetime, pattern: str, interval: int = 1) -> datetime:
    """
    Calculate the next occurrence date based on the recurrence pattern.
    
    Args:
        due_date: The original due date
        pattern: The recurrence pattern ('daily', 'weekly', 'monthly')
        interval: The interval (e.g., every 2 weeks)
    
    Returns:
        datetime: The calculated next occurrence date
    """
    if pattern == "daily":
        return due_date + timedelta(days=interval)
    elif pattern == "weekly":
        return due_date + timedelta(weeks=interval)
    elif pattern == "monthly":
        # For monthly recurrence, we add months
        # This is a simplified approach - in production, you'd want to handle month boundaries properly
        import calendar
        year = due_date.year
        month = due_date.month + interval
        
        # Handle year overflow
        while month > 12:
            year += 1
            month -= 12
            
        # Handle day overflow (e.g., Jan 31 + 1 month should be Feb 28/29, not Mar 3)
        max_day = calendar.monthrange(year, month)[1]
        day = min(due_date.day, max_day)
        
        return due_date.replace(year=year, month=month, day=day)
    else:
        raise ValueError(f"Unsupported recurrence pattern: {pattern}")


def create_next_recurring_task(original_task: Task) -> Task:
    """
    Create the next occurrence of a recurring task.
    
    Args:
        original_task: The original recurring task that was completed
    
    Returns:
        Task: The newly created task for the next occurrence
    """
    # Calculate the next occurrence date
    next_due_date = calculate_next_occurrence(
        original_task.due_date,
        original_task.recurrence_pattern,
        original_task.recurrence_interval
    )
    
    # Create a new task with the same properties as the original
    next_task = Task(
        title=original_task.title,
        description=original_task.description,
        completed=False,  # New occurrence is not completed
        user_id=original_task.user_id,
        priority=original_task.priority,
        tags=original_task.tags,
        due_date=next_due_date,
        reminder_time=original_task.reminder_time,
        recurrence_pattern=original_task.recurrence_pattern,
        recurrence_interval=original_task.recurrence_interval,
        parent_task_id=original_task.id  # Link to the original task
    )
    
    # Save the new task to the database
    with Session(engine) as session:
        session.add(next_task)
        session.commit()
        session.refresh(next_task)
    
    logger.info(f"Created next occurrence of recurring task {original_task.id}: new task {next_task.id}")
    return next_task


async def consume_task_events():
    """Consume task events from Kafka and process recurring task logic."""
    consumer = KafkaConsumer(
        TASK_EVENTS_TOPIC,
        bootstrap_servers=[KAFKA_BROKERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='recurring-task-service-group'
    )
    
    logger.info(f"Started consuming from {TASK_EVENTS_TOPIC}")
    
    for message in consumer:
        try:
            event_data = message.value
            event_type = event_data.get('event_type')
            task_id = event_data.get('task_id')
            
            logger.info(f"Received {event_type} event for task {task_id}")
            
            # Only process 'completed' events for recurring tasks
            if event_type == 'completed':
                task_data = event_data.get('task_data', {})
                
                # Check if this task has recurrence settings
                recurrence_pattern = task_data.get('recurrence_pattern')
                if recurrence_pattern:
                    logger.info(f"Processing recurring task completion: {task_id}")
                    
                    # Get the task from the database to ensure we have the latest data
                    with Session(engine) as session:
                        task = session.exec(select(Task).where(Task.id == task_id)).first()
                        
                        if task and task.recurrence_pattern:
                            # Create the next occurrence
                            next_task = create_next_recurring_task(task)
                            
                            # TODO: Publish event for the newly created task
                            # This would typically publish to the task-events topic
                            logger.info(f"Successfully created next occurrence: {next_task.id}")
            
        except Exception as e:
            logger.error(f"Error processing task event: {str(e)}", exc_info=True)


@dapr_app.subscribe(pubsub='kafka-pubsub', topic='task-events')
async def handle_task_event(event_data: Dict[str, Any]) -> None:
    """
    Handle task events via Dapr pub/sub.
    This is an alternative to the direct Kafka consumer approach.
    """
    try:
        event_type = event_data.get('event_type')
        task_id = event_data.get('task_id')
        
        logger.info(f"Dapr received {event_type} event for task {task_id}")
        
        # Only process 'completed' events for recurring tasks
        if event_type == 'completed':
            task_data = event_data.get('task_data', {})
            
            # Check if this task has recurrence settings
            recurrence_pattern = task_data.get('recurrence_pattern')
            if recurrence_pattern:
                logger.info(f"Processing recurring task completion via Dapr: {task_id}")
                
                # Get the task from the database to ensure we have the latest data
                with Session(engine) as session:
                    task = session.exec(select(Task).where(Task.id == task_id)).first()
                    
                    if task and task.recurrence_pattern:
                        # Create the next occurrence
                        next_task = create_next_recurring_task(task)
                        
                        logger.info(f"Successfully created next occurrence via Dapr: {next_task.id}")
    
    except Exception as e:
        logger.error(f"Error processing task event via Dapr: {str(e)}", exc_info=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Recurring Task Service is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "recurring-task-service"}