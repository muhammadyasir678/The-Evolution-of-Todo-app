# API Contract: Phase I - In-Memory Python Console App

## Overview
This document describes the internal API contracts for the console todo application. These represent the function signatures and expected behaviors of the core components.

## Task Manager Interface

### Create Task
- **Function**: `create_task(title: str, description: str = "") -> Task`
- **Parameters**:
  - `title`: Required string (1-200 chars)
  - `description`: Optional string (max 1000 chars)
- **Returns**: Task object with auto-generated ID and default status
- **Behavior**: Creates new task with unique ID and sets completion status to False

### Get Task
- **Function**: `get_task(task_id: int) -> Optional[Task]`
- **Parameters**:
  - `task_id`: Positive integer representing task ID
- **Returns**: Task object if found, None if not found
- **Behavior**: Retrieves task by ID from in-memory storage

### Get All Tasks
- **Function**: `get_all_tasks() -> List[Task]`
- **Parameters**: None
- **Returns**: List of all Task objects
- **Behavior**: Returns all tasks in storage, empty list if none exist

### Update Task
- **Function**: `update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool`
- **Parameters**:
  - `task_id`: Positive integer representing task ID
  - `title`: Optional new title (1-200 chars)
  - `description`: Optional new description (max 1000 chars)
- **Returns**: True if successful, False if task not found
- **Behavior**: Updates specified fields of existing task

### Delete Task
- **Function**: `delete_task(task_id: int) -> bool`
- **Parameters**:
  - `task_id`: Positive integer representing task ID
- **Returns**: True if successful, False if task not found
- **Behavior**: Removes task from storage

### Toggle Task Completion
- **Function**: `toggle_task_completion(task_id: int) -> bool`
- **Parameters**:
  - `task_id`: Positive integer representing task ID
- **Returns**: True if successful, False if task not found
- **Behavior**: Toggles completion status of task

### Validate Task Data
- **Function**: `validate_task_data(title: str, description: str = "") -> Tuple[bool, List[str]]`
- **Parameters**:
  - `title`: String to validate as title
  - `description`: String to validate as description
- **Returns**: Tuple of (is_valid, list_of_errors)
- **Behavior**: Validates input data against business rules

## Task Model Contract

### Task Object Properties
- `id`: int (immutable after creation)
- `title`: str (validatable)
- `description`: str (optional)
- `completed`: bool (mutable)
- `created_at`: datetime (immutable after creation)