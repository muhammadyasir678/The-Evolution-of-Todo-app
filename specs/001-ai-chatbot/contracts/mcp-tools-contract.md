# API Contract: MCP Tools

## Overview
The MCP server exposes 5 tools for task management operations. These tools are accessed by the OpenAI Agent through the MCP protocol.

## Tool: add_task

### Description
Creates a new task for the specified user.

### Parameters
- `user_id` (string, required): The ID of the user for whom to create the task
- `title` (string, required): The title of the task
- `description` (string, optional): Additional details about the task

### Response
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Buy groceries"
}
```

### Response Properties
- `task_id` (integer): The ID of the newly created task
- `status` (string): Confirmation status ("created")
- `title` (string): The title of the created task

---

## Tool: list_tasks

### Description
Retrieves tasks for the specified user.

### Parameters
- `user_id` (string, required): The ID of the user whose tasks to retrieve
- `status` (string, optional): Filter tasks by status ("all", "pending", "completed")
  - Default: "all"

### Response
```json
{
  "tasks": [
    {
      "id": 123,
      "title": "Buy groceries",
      "completed": false,
      "description": "Get milk, bread, eggs"
    },
    {
      "id": 124,
      "title": "Call mom",
      "completed": true,
      "description": "Catch up on family news"
    }
  ]
}
```

### Response Properties
- `tasks` (array[object]): List of task objects
  - `id` (integer): Task identifier
  - `title` (string): Task title
  - `completed` (boolean): Completion status
  - `description` (string): Task description

---

## Tool: complete_task

### Description
Marks a specific task as completed for the specified user.

### Parameters
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to mark as complete

### Response
```json
{
  "task_id": 123,
  "status": "completed",
  "title": "Buy groceries"
}
```

### Response Properties
- `task_id` (integer): The ID of the completed task
- `status` (string): Confirmation status ("completed")
- `title` (string): The title of the completed task

---

## Tool: delete_task

### Description
Removes a specific task for the specified user.

### Parameters
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to delete

### Response
```json
{
  "task_id": 123,
  "status": "deleted",
  "title": "Buy groceries"
}
```

### Response Properties
- `task_id` (integer): The ID of the deleted task
- `status` (string): Confirmation status ("deleted")
- `title` (string): The title of the deleted task

---

## Tool: update_task

### Description
Modifies an existing task for the specified user.

### Parameters
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task

### Response
```json
{
  "task_id": 123,
  "status": "updated",
  "title": "Buy groceries and cook dinner"
}
```

### Response Properties
- `task_id` (integer): The ID of the updated task
- `status` (string): Confirmation status ("updated")
- `title` (string): The updated title of the task

---

## Common Error Responses

### Error Format
```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Detailed error message"
  }
}
```

### Error Types
- `invalid_request_error`: Invalid parameters provided
- `authentication_error`: Invalid user_id or unauthorized access
- `not_found_error`: Task or user not found
- `server_error`: Internal server error occurred