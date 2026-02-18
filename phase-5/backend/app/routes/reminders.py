from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta, timezone
from ..database import get_session
from ..models import Task, TaskPublic
from ..auth import get_current_user
from ..dapr_publisher import publish_reminder_event

router = APIRouter(prefix="/api", tags=["reminders"])


@router.post("/reminders/check")
def check_due_reminders(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Check for tasks with due reminders and publish reminder events.
    This endpoint would be called by a cron job or scheduled task.

    Args:
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        dict: Status of the reminder check operation
    """
    # Find tasks with reminder times that are due now or in the past
    # We'll check for reminders that should have been sent in the last 5 minutes
    # to account for any delays in the cron job execution
    now = datetime.now(timezone.utc)
    five_minutes_ago = now - timedelta(minutes=5)

    statement = select(Task).where(
        Task.reminder_time != None,  # Correct SQLModel syntax to check for non-NULL
        Task.reminder_time <= now,
        Task.reminder_time >= five_minutes_ago,
        Task.completed == False
    )

    due_tasks = session.exec(statement).all()

    reminder_count = 0
    for task in due_tasks:
        # Publish reminder event to Kafka via Dapr
        try:
            task_dict = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "priority": task.priority,
                "tags": task.tags,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
                "recurrence_pattern": task.recurrence_pattern,
                "recurrence_interval": task.recurrence_interval,
                "parent_task_id": task.parent_task_id
            }

            publish_reminder_event(task_dict)
            reminder_count += 1

        except Exception as e:
            # Log the error but continue processing other tasks
            print(f"Error publishing reminder event for task {task.id}: {str(e)}")

    return {
        "status": "success",
        "message": f"Checked for due reminders, published {reminder_count} reminder events",
        "checked_at": datetime.now(timezone.utc).isoformat()
    }


@router.post("/reminders/cron-handler")
async def handle_cron_reminders(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Dapr cron binding handler that gets called based on the cron schedule.
    This endpoint is triggered by the Dapr cron binding.

    Args:
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        dict: Status of the cron handler operation
    """
    # Find tasks with reminder times that are due now or in the past
    # We'll check for reminders that should have been sent in the last 5 minutes
    # to account for any delays in the cron job execution
    now = datetime.now(timezone.utc)
    five_minutes_ago = now - timedelta(minutes=5)

    statement = select(Task).where(
        Task.reminder_time != None,  # Correct SQLModel syntax to check for non-NULL
        Task.reminder_time <= now,
        Task.reminder_time >= five_minutes_ago,
        Task.completed == False
    )

    due_tasks = session.exec(statement).all()

    reminder_count = 0
    for task in due_tasks:
        # Publish reminder event to Kafka via Dapr
        try:
            task_dict = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "priority": task.priority,
                "tags": task.tags,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
                "recurrence_pattern": task.recurrence_pattern,
                "recurrence_interval": task.recurrence_interval,
                "parent_task_id": task.parent_task_id
            }

            publish_reminder_event(task_dict)
            reminder_count += 1

        except Exception as e:
            # Log the error but continue processing other tasks
            print(f"Error publishing reminder event for task {task.id}: {str(e)}")

    return {
        "status": "success",
        "message": f"Cron reminder handler executed successfully, processed {reminder_count} reminders",
        "executed_at": datetime.now(timezone.utc).isoformat()
    }