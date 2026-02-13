"""
Audit Service
This service consumes task events from Kafka and logs them to the audit log table.
It maintains a record of all operations performed on tasks for compliance and tracking.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI
from kafka import KafkaConsumer
from sqlmodel import Session, select, create_engine, SQLModel, Field, desc
from sqlalchemy import Column, DateTime, Enum as saEnum
import sqlalchemy as sa
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine
engine = create_engine(DATABASE_URL)

# Define local models to avoid circular dependencies
from typing import Optional

class AuditLog(SQLModel, table=True):
    """
    AuditLog model for tracking all task operations.
    """
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(index=True)  # Reference to user
    task_id: Optional[int] = Field(default=None, index=True)  # Reference to task
    action: str = Field(sa_column=Column(saEnum("created", "updated", "deleted", "completed", name="action_enum")))  # Action performed
    details: Optional[str] = Field(default=None)  # JSON field for task data or changes
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # Timestamp of the event
    correlation_id: Optional[str] = Field(default=None)  # For tracking related events in event flows

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Audit Service")

# Initialize Dapr extension
dapr_app = DaprApp(app)

# Kafka consumer configuration
KAFKA_BROKERS = "kafka.kafka.svc.cluster.local:9092"
TASK_EVENTS_TOPIC = "task-events"


@app.on_event("startup")
async def startup_event():
    """Initialize the Kafka consumer and start listening for events."""
    logger.info("Starting Audit Service...")
    # Create all tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    # Start the Kafka consumer in a background task
    asyncio.create_task(consume_task_events())


def log_audit_entry(event_data: Dict[str, Any]):
    """
    Log the event to the audit log table.
    
    Args:
        event_data: The event data received from Kafka
    """
    try:
        event_type = event_data.get('event_type')
        user_id = event_data.get('user_id')
        task_id = event_data.get('task_id')
        task_data = event_data.get('task_data', {})
        timestamp = event_data.get('timestamp')
        correlation_id = event_data.get('correlation_id', '')

        # Skip if critical fields are missing
        if user_id is None:
            logger.warning("Event missing user_id, skipping audit log entry")
            return

        # Create an audit log entry
        audit_entry = AuditLog(
            user_id=user_id,
            task_id=task_id if task_id is not None else None,
            action=event_type if event_type is not None else "unknown",
            details=json.dumps(task_data),  # Store the full task data as JSON
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')) if timestamp else datetime.utcnow(),
            correlation_id=correlation_id
        )

        # Save the audit entry to the database
        with Session(engine) as session:
            session.add(audit_entry)
            session.commit()

        logger.info(f"Audit log created for user {user_id}, task {task_id}, action {event_type}")
        
    except Exception as e:
        logger.error(f"Error creating audit log entry: {str(e)}", exc_info=True)


async def consume_task_events():
    """Consume task events from Kafka and log them to the audit table."""
    consumer = KafkaConsumer(
        TASK_EVENTS_TOPIC,
        bootstrap_servers=[KAFKA_BROKERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='audit-service-group'
    )
    
    logger.info(f"Started consuming from {TASK_EVENTS_TOPIC}")
    
    for message in consumer:
        try:
            event_data = message.value
            event_type = event_data.get('event_type')
            task_id = event_data.get('task_id')
            
            logger.info(f"Received {event_type} event for task {task_id}")
            
            # Log the event to the audit table
            log_audit_entry(event_data)
            
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
        
        # Log the event to the audit table
        log_audit_entry(event_data)
    
    except Exception as e:
        logger.error(f"Error processing task event via Dapr: {str(e)}", exc_info=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Audit Service is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit-service"}


@app.get("/audit-logs/{user_id}")
def get_audit_logs_for_user(user_id: str):
    """Retrieve audit logs for a specific user."""
    try:
        with Session(engine) as session:
            statement = select(AuditLog).where(AuditLog.user_id == user_id).order_by(desc(AuditLog.timestamp))
            audit_logs = session.exec(statement).all()
            return audit_logs
    except Exception as e:
        logger.error(f"Error retrieving audit logs for user {user_id}: {str(e)}", exc_info=True)
        return []


@app.get("/audit-logs/task/{task_id}")
def get_audit_logs_for_task(task_id: int):
    """Retrieve audit logs for a specific task."""
    try:
        with Session(engine) as session:
            statement = select(AuditLog).where(AuditLog.task_id == task_id).order_by(desc(AuditLog.timestamp))
            audit_logs = session.exec(statement).all()
            return audit_logs
    except Exception as e:
        logger.error(f"Error retrieving audit logs for task {task_id}: {str(e)}", exc_info=True)
        return []