# AI-Powered Todo Chatbot - Phase III

This is the implementation of the AI-Powered Todo Chatbot featuring natural language interaction with the todo list using OpenAI's tools and MCP server architecture.

## Architecture Overview

The system consists of three main components:

1. **MCP Server** - Implements the MCP tools for task operations
2. **Backend** - FastAPI application with chat endpoint and OpenAI Agent integration
3. **Frontend** - Next.js application with ChatKit UI for natural language interaction

## Components

### MCP Server (`mcp-server/`)
- Implements 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Connects to the database to perform operations
- Enforces user isolation (user A cannot access user B's tasks)
- Stateless architecture

### Backend (`backend/`)
- FastAPI application
- Chat endpoint at `/api/{user_id}/chat`
- OpenAI Agent integration
- Database models for Conversation and Message entities
- JWT authentication

### Frontend (`frontend/`)
- Next.js 16+ application with TypeScript and Tailwind CSS
- Chat interface using OpenAI ChatKit
- Protected routes for authenticated users
- Real-time messaging interface

## Database Models

### New Models (in addition to Phase II Task model)
- **Conversation**: Stores chat session metadata
  - id, user_id, created_at, updated_at
- **Message**: Stores individual chat messages
  - id, user_id, conversation_id, role (user/assistant), content, created_at

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 18+
- uv package manager
- Neon PostgreSQL database
- OpenAI API key

### MCP Server Setup
```bash
cd mcp-server/
uv init
uv add mcp openai psycopg2-binary sqlmodel pydantic
```

Create `.env` with:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
OPENAI_API_KEY=sk-your-openai-api-key
```

### Backend Setup
```bash
cd backend/
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add fastapi uvicorn sqlmodel openai python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv
```

Create `.env` with:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
OPENAI_API_KEY=sk-your-openai-api-key
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Setup
```bash
cd frontend/
npm install
npm install @openai/chatkit
```

Create `.env.local` with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

### OpenAI API Key Configuration
Task T102: Update documentation with OpenAI API key configuration instructions

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add it to your environment files:
   - MCP Server: `mcp-server/.env` - `OPENAI_API_KEY=sk-your-openai-api-key`
   - Backend: `backend/.env` - `OPENAI_API_KEY=sk-your-openai-api-key`
3. Ensure your OpenAI account has sufficient credits and the required permissions
4. For production, use a secure method to store the API key (environment variables, secret management system)

### OpenAI ChatKit Domain Allowlist Setup
Task T103: Update documentation with OpenAI ChatKit domain allowlist setup

1. Deploy your frontend application to a production domain (e.g., Vercel, Netlify)
2. Go to [OpenAI Platform Settings](https://platform.openai.com/settings)
3. Navigate to Security → Domain Allowlist
4. Add your production domain (e.g., `https://your-app.vercel.app`)
5. Save the settings
6. Copy the domain key that appears after saving
7. Update your frontend environment variables:
   - In `.env.local`: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key`
8. For development, localhost typically works without adding to the allowlist
9. For multiple environments (staging, prod), add each domain separately

### Task T100: Configure OpenAI domain allowlist for production deployment
1. Deploy frontend to production (e.g., Vercel)
2. Go to OpenAI platform: Settings → Security → Domain Allowlist
3. Add your production URL (e.g., https://your-app.vercel.app)
4. Copy the domain key and set it as NEXT_PUBLIC_OPENAI_DOMAIN_KEY
5. Update environment variables in your hosting platform:
   - Vercel: Go to Project Settings → Environment Variables
   - Netlify: Go to Site Settings → Build & Deploy → Environment
   - Other platforms: Similar environment variable configuration
6. Redeploy your application after updating the environment variables
7. Test that the ChatKit UI loads correctly in production

## Running the Application

### 1. Start MCP Server
```bash
cd mcp-server/
uv run src/server.py
```

### 2. Start Backend
```bash
cd backend/
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend
```bash
cd frontend/
npm run dev
```

## API Documentation

### Chat Endpoint
Task T120: Complete API documentation for chat endpoint

**Endpoint**: `POST /api/{user_id}/chat`

**Description**: Processes natural language messages through the AI assistant and manages tasks using MCP tools.

**Path Parameters**:
- `user_id` (string): The ID of the authenticated user

**Request Body**:
```json
{
  "conversation_id": 123, // Optional: existing conversation ID, null for new
  "message": "Add a task to buy milk" // Required: user's message in natural language
}
```

**Response**:
```json
{
  "conversation_id": 123, // ID of the conversation (new or existing)
  "response": "I've added 'buy milk' to your tasks.", // AI-generated response
  "tool_calls": ["add_task"] // Array of MCP tools that were invoked
}
```

**Authentication**: JWT token required in Authorization header: `Bearer {token}`

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User trying to access another user's chat
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Error processing request with AI agent

## Natural Language Commands Supported

Task T122: Create user guide for natural language commands

The AI assistant understands various natural language commands:

### Adding Tasks
- "Add a task to buy milk"
- "Create a task to call the doctor"
- "I need to remember to pay bills"
- "Add task: finish the report"

### Listing Tasks
- "Show me my tasks"
- "What tasks do I have?"
- "Show all my tasks"
- "What's pending?"
- "Show incomplete tasks"
- "Show completed tasks"

### Completing Tasks
- "Mark task 1 as complete"
- "Complete the shopping task"
- "Finish task 3"
- "Mark 'buy groceries' as done"

### Deleting Tasks
- "Delete task 2"
- "Remove the meeting task"
- "Delete 'buy milk'"
- "Cancel task 1"

### Updating Tasks
- "Change task 1 to 'Call mom tonight'"
- "Update task 3 description to 'Important meeting'"
- "Rename 'groceries' to 'weekly groceries'"
- "Edit task 2 title to 'Finish project'"

## Command Structure Tips
- Be clear about the task ID when referencing specific tasks
- Use descriptive titles for better organization
- You can combine multiple requests in one message
- The AI will confirm important actions before completing them

## MCP Tool Specifications
Task T121: Document MCP tool specifications and parameters

The AI assistant integrates with the following MCP tools:

### add_task
- **Parameters**: user_id (string), title (string), description (string, optional)
- **Function**: Creates a new task for the specified user
- **Returns**: task_id and success message

### list_tasks
- **Parameters**: user_id (string), status (string: "all", "completed", "pending", optional)
- **Function**: Lists tasks for the specified user with optional status filter
- **Returns**: Array of tasks with their properties

### complete_task
- **Parameters**: user_id (string), task_id (integer)
- **Function**: Marks the specified task as completed
- **Returns**: task_id and confirmation

### delete_task
- **Parameters**: user_id (string), task_id (integer)
- **Function**: Deletes the specified task
- **Returns**: task_id and confirmation

### update_task
- **Parameters**: user_id (string), task_id (integer), title (string, optional), description (string, optional)
- **Function**: Updates the specified task with new values
- **Returns**: updated task_id and values

## Features

- Natural language task management
- Persistent conversations stored in database
- User isolation (each user has independent tasks/conversations)
- Stateless architecture (can restart servers without losing context)
- OpenAI ChatKit frontend integration
- JWT authentication for security

## Database Migrations

Run the migration script to create the new tables:
```bash
cd backend/
python -m migrations
```