"""
Chat API Endpoint - Tasks T036, T037, T038, T039
Implement POST /api/{user_id}/chat endpoint with JWT authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, asc
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

from app.database import get_session
from ..auth import get_current_user
from ..models import (
    Message, MessageCreate, MessagePublic,
    Conversation, ConversationCreate, ConversationPublic
)
from ..agent import run_agent

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Task T036: Implement POST /api/{user_id}/chat endpoint that accepts conversation_id (optional) and message (required)
    Task T037: Add JWT authentication to chat endpoint using get_current_user
    Task T038: Implement logic to create new Conversation if conversation_id is null
    Task T039: Implement logic to fetch conversation history from messages table
    """

    # Verify that the user_id in the path matches the authenticated user
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's chat"
        )

    conversation_id = chat_request.conversation_id

    # If no conversation_id is provided, create a new conversation
    if conversation_id is None:
        # Create a new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id
    else:
        # Verify that the conversation belongs to the user
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

    # Store the user's message in the database
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=chat_request.message
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)

    # Fetch conversation history from messages table
    # Get all messages in this conversation ordered by creation time
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(asc(Message.created_at))
    messages_db = session.exec(statement).all()

    # Convert messages to the format expected by the agent
    messages_for_agent = []
    for msg in messages_db:
        messages_for_agent.append({
            "role": msg.role,
            "content": msg.content
        })

    # Task T050: Enhance chat endpoint to build message array combining history and new message
    # The message array is already built as messages_for_agent above

    # Task T051: Enhance chat endpoint to call agent with messages and process responses
    try:
        agent_response = run_agent(messages_for_agent, user_id)
        response_text = agent_response["response"]
        tool_calls = agent_response["tool_calls"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request with AI agent: {str(e)}"
        )

    # Task T052: Enhance chat endpoint to store user message in database
    # Already implemented above when we stored the user's message

    # Task T053: Enhance chat endpoint to store assistant response in database
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=response_text
    )
    session.add(assistant_message)
    session.commit()

    # Task T054: Enhance chat endpoint to return conversation_id, response, and tool_calls
    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=tool_calls
    )