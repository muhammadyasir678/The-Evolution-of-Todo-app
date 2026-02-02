# API Contract: Chat Endpoint

## Endpoint: POST /api/{user_id}/chat

### Description
Accepts a user message and returns an AI-generated response. The endpoint handles conversation persistence by storing messages in the database and maintaining context across requests.

### Parameters
- **Path Parameter**:
  - `user_id` (string, required): The ID of the authenticated user making the request

### Request Body
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Request Body Properties**:
- `conversation_id` (integer | null, optional):
  - If provided, continues an existing conversation
  - If null, creates a new conversation
  - Default: null
- `message` (string, required):
  - The user's message to process
  - Maximum length: 10,000 characters

### Headers
- `Authorization: Bearer {jwt_token}` (required): Valid JWT token for authentication
- `Content-Type: application/json` (required): Request body format

### Response
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your tasks",
  "tool_calls": ["add_task"]
}
```

**Response Properties**:
- `conversation_id` (integer): The ID of the conversation (newly created or existing)
- `response` (string): The AI-generated response to the user's message
- `tool_calls` (array[string]): List of MCP tools that were invoked during processing

### Success Response
- **Status Code**: 200 OK
- **Content-Type**: application/json

### Error Responses
- **400 Bad Request**: Invalid request body format or missing required fields
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User attempting to access another user's conversations
- **422 Unprocessable Entity**: Validation error for request parameters
- **500 Internal Server Error**: Server-side processing error

### Example Requests

**Starting a new conversation**:
```json
{
  "conversation_id": null,
  "message": "Add a task to buy groceries"
}
```

**Continuing an existing conversation**:
```json
{
  "conversation_id": 123,
  "message": "Show me my tasks"
}
```

### Security
- JWT token must match the user_id in the path parameter
- User isolation enforced: users cannot access other users' conversations
- Rate limiting applied to prevent abuse

### Performance Expectations
- Response time: <3 seconds for 95% of requests
- Concurrent connections: Up to 1000 simultaneous users