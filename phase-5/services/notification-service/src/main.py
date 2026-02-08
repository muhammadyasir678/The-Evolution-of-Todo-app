"""
Notification Service
This service consumes reminder events from Kafka and sends notifications to users.
Supports both browser push notifications and email notifications.
"""

import asyncio
import json
import logging
from typing import Dict, Any

from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI
from kafka import KafkaConsumer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Notification Service")

# Initialize Dapr extension
dapr_app = DaprApp(app)

# Kafka consumer configuration
KAFKA_BROKERS = "kafka.kafka.svc.cluster.local:9092"
REMINDERS_TOPIC = "reminders"


@app.on_event("startup")
async def startup_event():
    """Initialize the Kafka consumer and start listening for reminder events."""
    logger.info("Starting Notification Service...")
    # Start the Kafka consumer in a background task
    asyncio.create_task(consume_reminder_events())


async def send_browser_notification(user_id: str, title: str, message: str):
    """
    Send a browser push notification to the user.
    In a real implementation, this would connect to the WebSocket service
    or use a push notification service like Firebase Cloud Messaging.
    """
    logger.info(f"Sending browser notification to user {user_id}: {title} - {message}")
    # In a real implementation, this would connect to the WebSocket service
    # to push the notification to the user's connected browsers
    # For now, we'll just log the notification
    pass


async def send_email_notification(user_id: str, recipient_email: str, subject: str, body: str):
    """
    Send an email notification to the user.
    In a real implementation, this would use a service like SendGrid or AWS SES.
    """
    logger.info(f"Sending email notification to {recipient_email}: {subject}")
    
    # In a real implementation, this would connect to an email service
    # For now, we'll just simulate the email sending
    try:
        # This is a placeholder - in production, use SendGrid, AWS SES, or similar
        logger.info(f"Email notification prepared for {recipient_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        
        # In a real implementation, you would do something like:
        # sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        # ...
        # response = sg.send(message)
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")


async def process_reminder_event(event_data: Dict[str, Any]):
    """
    Process a reminder event and send appropriate notifications.
    """
    try:
        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')
        title = event_data.get('title')
        due_at = event_data.get('due_at')
        notification_preferences = event_data.get('notification_preferences', {})
        
        logger.info(f"Processing reminder for task {task_id}, user {user_id}")
        
        # Prepare notification message
        message = f"Reminder: Your task '{title}' is due at {due_at}"
        
        # Send browser notification if enabled
        if notification_preferences.get('browser_push', False):
            await send_browser_notification(user_id, f"Task Reminder: {title}", message)
        
        # Send email notification if enabled
        if notification_preferences.get('email', False):
            # In a real implementation, we would look up the user's email address
            # For now, we'll use a placeholder
            user_email = f"{user_id}@example.com"
            await send_email_notification(
                user_id, 
                user_email, 
                f"Reminder: {title}", 
                message
            )
        
        logger.info(f"Notifications sent for task {task_id}")
        
    except Exception as e:
        logger.error(f"Error processing reminder event: {str(e)}", exc_info=True)


async def consume_reminder_events():
    """Consume reminder events from Kafka and process them."""
    consumer = KafkaConsumer(
        REMINDERS_TOPIC,
        bootstrap_servers=[KAFKA_BROKERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='notification-service-group'
    )
    
    logger.info(f"Started consuming from {REMINDERS_TOPIC}")
    
    for message in consumer:
        try:
            event_data = message.value
            await process_reminder_event(event_data)
        except Exception as e:
            logger.error(f"Error processing reminder event: {str(e)}", exc_info=True)


@dapr_app.subscribe(pubsub='kafka-pubsub', topic='reminders')
async def handle_reminder_event(event_data: Dict[str, Any]) -> None:
    """
    Handle reminder events via Dapr pub/sub.
    This is an alternative to the direct Kafka consumer approach.
    """
    try:
        await process_reminder_event(event_data)
    except Exception as e:
        logger.error(f"Error processing reminder event via Dapr: {str(e)}", exc_info=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Notification Service is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notification-service"}