from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic
from ..auth import get_current_user

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskPublic])
def get_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the specified user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        List[TaskPublic]: A list of tasks belonging to the user

    Raises:
        HTTPException: If the user_id in URL doesn't match the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    # Query tasks for the authenticated user
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.

    Args:
        user_id: The ID of the user creating the task
        task: Task creation request containing title and description
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        TaskPublic: The created task

    Raises:
        HTTPException: If the user_id in URL doesn't match the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create tasks for another user"
        )

    # Create the new task
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for the specified user.

    Args:
        user_id: The ID of the user whose task to retrieve
        task_id: The ID of the task to retrieve
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        TaskPublic: The requested task

    Raises:
        HTTPException: If the user_id doesn't match, or if the task doesn't exist
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's task"
        )

    # Get the task from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return db_task


@router.put("/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the specified user.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to update
        task_update: Task update request containing fields to update
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        TaskPublic: The updated task

    Raises:
        HTTPException: If the user_id doesn't match, or if the task doesn't exist
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's task"
        )

    # Get the task from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(db_task, field):
            setattr(db_task, field, value)
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the specified user.

    Args:
        user_id: The ID of the user whose task to delete
        task_id: The ID of the task to delete
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Raises:
        HTTPException: If the user_id doesn't match, or if the task doesn't exist
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's task"
        )

    # Get the task from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    session.delete(db_task)
    session.commit()


@router.patch("/tasks/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the specified user.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to update
        task_update: Task update request containing the completed status
        current_user_id: The ID of the currently authenticated user (from JWT)
        session: Database session

    Returns:
        TaskPublic: The updated task

    Raises:
        HTTPException: If the user_id doesn't match, or if the task doesn't exist
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's task"
        )

    # Get the task from the database
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task's completion status
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task