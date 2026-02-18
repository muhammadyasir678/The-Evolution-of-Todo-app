"""
WebSocket API for real-time task updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# Store active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)

    async def broadcast_to_user(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(json.dumps(message))

    def get_connected_users(self):
        return list(self.active_connections.keys())

manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time updates for a specific user
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Send a welcome message
        welcome_msg = {
            "type": "connection",
            "message": f"Connected to WebSocket for user {user_id}",
            "user_id": user_id
        }
        await manager.send_personal_message(json.dumps(welcome_msg), user_id)
        
        # Listen for messages from the client
        while True:
            # In this implementation, we're primarily sending updates to the client
            # rather than receiving messages from it
            data = await websocket.receive_text()
            
            # Parse the received message
            try:
                message = json.loads(data)
                
                # Echo the message back to the user
                response = {
                    "type": "echo",
                    "original_message": message,
                    "user_id": user_id
                }
                await manager.send_personal_message(json.dumps(response), user_id)
                
            except json.JSONDecodeError:
                # If it's not JSON, send it back as a simple echo
                response = {
                    "type": "echo",
                    "original_message": data,
                    "user_id": user_id
                }
                await manager.send_personal_message(json.dumps(response), user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"WebSocket disconnected for user {user_id}")


async def notify_user_task_change(user_id: str, task_data: dict, action: str):
    """
    Function to notify a user about a task change
    
    Args:
        user_id: The ID of the user to notify
        task_data: The task data that changed
        action: The action that occurred (create, update, delete, complete, etc.)
    """
    message = {
        "type": "task_update",
        "action": action,
        "task_data": task_data,
        "user_id": user_id,
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Broadcast to the specific user
    await manager.broadcast_to_user(message, user_id)