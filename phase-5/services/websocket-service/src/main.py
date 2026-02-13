"""
WebSocket Service
This service maintains WebSocket connections with clients and broadcasts task updates.
It consumes task-update events from Kafka and forwards them to connected clients.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Set
from collections import defaultdict

from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from kafka import KafkaConsumer
import websockets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="WebSocket Service")

# Initialize Dapr extension
dapr_app = DaprApp(app)

# Kafka consumer configuration
KAFKA_BROKERS = "kafka.kafka.svc.cluster.local:9092"
TASK_UPDATES_TOPIC = "task-updates"

# Store active WebSocket connections by user
active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected. Total connections for user: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id].discard(websocket)
        logger.info(f"User {user_id} disconnected. Remaining connections: {len(self.active_connections[user_id])}")
        if len(self.active_connections[user_id]) == 0:
            del self.active_connections[user_id]

    async def broadcast_to_user(self, message: Dict[str, Any], user_id: str):
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except WebSocketDisconnect:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.disconnect(connection, user_id)
                
            logger.info(f"Broadcasted message to {user_id}: {len(self.active_connections[user_id])} connections")


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Handle WebSocket connections for a specific user."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Just keep the connection alive
            # Clients send messages to notify server of their presence
            data = await websocket.receive_text()
            # Optionally, process any messages from client
            logger.debug(f"Received message from user {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


@app.on_event("startup")
async def startup_event():
    """Initialize the Kafka consumer and start listening for task update events."""
    logger.info("Starting WebSocket Service...")
    # Start the Kafka consumer in a background task
    asyncio.create_task(consume_task_updates())


async def consume_task_updates():
    """Consume task update events from Kafka and broadcast to connected clients."""
    consumer = KafkaConsumer(
        TASK_UPDATES_TOPIC,
        bootstrap_servers=[KAFKA_BROKERS],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='websocket-service-group'
    )
    
    logger.info(f"Started consuming from {TASK_UPDATES_TOPIC}")
    
    for message in consumer:
        try:
            event_data = message.value
            user_id = event_data.get('user_id')

            # Skip if user_id is None
            if user_id is None:
                logger.warning("Task update event missing user_id, skipping broadcast")
                continue

            logger.info(f"Received task update for user {user_id}")

            # Broadcast the update to all connected clients for this user
            await manager.broadcast_to_user(event_data, user_id)

        except Exception as e:
            logger.error(f"Error processing task update event: {str(e)}", exc_info=True)


@dapr_app.subscribe(pubsub='kafka-pubsub', topic='task-updates')
async def handle_task_update_event(event_data: Dict[str, Any]) -> None:
    """
    Handle task update events via Dapr pub/sub.
    This is an alternative to the direct Kafka consumer approach.
    """
    try:
        user_id = event_data.get('user_id')

        # Skip if user_id is None
        if user_id is None:
            logger.warning("Dapr task update event missing user_id, skipping broadcast")
            return

        logger.info(f"Dapr received task update for user {user_id}")

        # Broadcast the update to all connected clients for this user
        await manager.broadcast_to_user(event_data, user_id)

    except Exception as e:
        logger.error(f"Error processing task update event via Dapr: {str(e)}", exc_info=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "WebSocket Service is running", "connections": sum(len(conns) for conns in manager.active_connections.values())}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "service": "websocket-service",
        "active_users": len(manager.active_connections),
        "total_connections": sum(len(conns) for conns in manager.active_connections.values())
    }