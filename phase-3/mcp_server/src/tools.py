"""
MCP tools implementation for AI-Powered Todo Chatbot - Tasks T020-T024
Contains all 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
"""
import asyncio
from mcp.server import Server
from mcp.types import TextContent
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlmodel import create_engine, Session, select
# Import models from backend - add backend to path
import sys
import os
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
from app.models import Task, TaskCreate, TaskUpdate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todo_app.db")
engine = create_engine(DATABASE_URL)

class AddTaskRequest(BaseModel):
    """Request model for add_task MCP tool."""
    user_id: str
    title: str
    description: Optional[str] = None

class ListTasksRequest(BaseModel):
    """Request model for list_tasks MCP tool."""
    user_id: str
    status: Optional[str] = None  # "all", "completed", "pending"

class CompleteTaskRequest(BaseModel):
    """Request model for complete_task MCP tool."""
    user_id: str
    task_id: int

class DeleteTaskRequest(BaseModel):
    """Request model for delete_task MCP tool."""
    user_id: str
    task_id: int

class UpdateTaskRequest(BaseModel):
    """Request model for update_task MCP tool."""
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None

async def add_task(request: AddTaskRequest) -> Dict[str, Any]:
    """
    MCP Tool T020: Implement add_task tool with parameters: user_id, title, description
    """
    with Session(engine) as session:
        try:
            # Create new task
            task_data = TaskCreate(
                title=request.title,
                description=request.description or "",
                completed=False
            )
            task = Task(
                **task_data.model_dump(),
                user_id=request.user_id
            )

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "message": f"Task '{task.title}' created successfully"
            }
        except Exception as e:
            session.rollback()
            # Task T055: Add proper error handling to MCP tools with structured responses
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create task"
            }

async def list_tasks(request: ListTasksRequest) -> Dict[str, Any]:
    """
    MCP Tool T021: Implement list_tasks tool with parameters: user_id, status
    """
    with Session(engine) as session:
        try:
            # Build query with user_id filter
            query = select(Task).where(Task.user_id == request.user_id)

            # Task T057: Enhance list_tasks tool to properly filter by status (completed/incomplete)
            # Apply status filter if provided
            if request.status == "completed":
                query = query.where(Task.completed == True)
            elif request.status == "pending":
                query = query.where(Task.completed == False)
            # For "all" or unspecified status, no additional filter needed

            tasks = session.exec(query).all()

            # Format response
            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                task_list.append(task_dict)

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list),
                "message": f"Retrieved {len(task_list)} tasks for user"
            }
        except Exception as e:
            # Task T055: Add proper error handling to MCP tools with structured responses
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve tasks"
            }

async def complete_task(request: CompleteTaskRequest) -> Dict[str, Any]:
    """
    MCP Tool T022: Implement complete_task tool with parameters: user_id, task_id
    """
    with Session(engine) as session:
        try:
            # Find task by ID and user_id (enforce user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == request.task_id,
                    Task.user_id == request.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {request.task_id} not found or access denied"
                }

            # Update task completion status
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "completed": task.completed,
                "message": f"Task '{task.title}' marked as complete"
            }
        except Exception as e:
            session.rollback()
            # Task T055: Add proper error handling to MCP tools with structured responses
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete task"
            }

async def delete_task(request: DeleteTaskRequest) -> Dict[str, Any]:
    """
    MCP Tool T023: Implement delete_task tool with parameters: user_id, task_id
    """
    with Session(engine) as session:
        try:
            # Find task by ID and user_id (enforce user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == request.task_id,
                    Task.user_id == request.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {request.task_id} not found or access denied"
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "task_id": request.task_id,
                "message": f"Task '{task.title}' deleted successfully"
            }
        except Exception as e:
            session.rollback()
            # Task T055: Add proper error handling to MCP tools with structured responses
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task"
            }

async def update_task(request: UpdateTaskRequest) -> Dict[str, Any]:
    """
    MCP Tool T024: Implement update_task tool with parameters: user_id, task_id, title, description
    """
    with Session(engine) as session:
        try:
            # Find task by ID and user_id (enforce user isolation)
            task = session.exec(
                select(Task).where(
                    Task.id == request.task_id,
                    Task.user_id == request.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {request.task_id} not found or access denied"
                }

            # Update task fields if provided
            if request.title is not None:
                task.title = request.title
            if request.description is not None:
                task.description = request.description

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "message": f"Task ID {task.id} updated successfully"
            }
        except Exception as e:
            session.rollback()
            # Task T055: Add proper error handling to MCP tools with structured responses
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task"
            }