# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites

- Python 3.13+
- Node.js 18+ with npm
- uv package manager (for Python dependency management)
- Neon PostgreSQL database account
- OpenAI API key
- OpenAI ChatKit domain key

## Setup Instructions

### 1. Clone and Navigate to Phase 3 Directory

```bash
cd /path/to/project/phase-3
```

### 2. Backend Setup (FastAPI)

```bash
cd backend/

# Install Python dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add fastapi uvicorn sqlmodel openai-agents-sdk python-jose[cryptography] passlib[bcrypt] python-multipart

# Create environment file
cp .env.example .env
# Edit .env with your database connection and API keys
```

#### Backend Environment Variables
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
OPENAI_API_KEY=sk-your-openai-api-key
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Frontend Setup (Next.js)

```bash
cd frontend/

# Install JavaScript dependencies
npm install
npm install @openai/chatkit

# Create environment file
cp .env.local.example .env.local
# Edit .env.local with your OpenAI domain key
```

#### Frontend Environment Variables
```
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-openai-domain-key
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

### 4. MCP Server Setup

```bash
cd mcp-server/

# Initialize project
uv init
uv add mcp openai psycopg2-binary

# Create environment file
cp .env.example .env
# Edit .env with your OpenAI API key and database connection
```

#### MCP Server Environment Variables
```
OPENAI_API_KEY=sk-your-openai-api-key
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
```

## Running the Application

### 1. Start MCP Server

```bash
cd mcp-server/
uv run src/server.py
```

### 2. Start Backend (FastAPI)

```bash
cd backend/
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend (Next.js)

```bash
cd frontend/
npm run dev
```

## API Endpoints

### Chat Endpoint
```
POST /api/{user_id}/chat
Headers: Authorization: Bearer {jwt_token}
Body: {
  "conversation_id": 123, // Optional, null creates new
  "message": "Add a task to buy groceries"
}
Response: {
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your tasks",
  "tool_calls": ["add_task"]
}
```

## OpenAI Configuration

### Domain Allowlist Setup
1. Deploy frontend to production (e.g., Vercel)
2. Go to OpenAI platform: Settings → Security → Domain Allowlist
3. Add your production URL (e.g., https://your-app.vercel.app)
4. Copy the domain key and set it as NEXT_PUBLIC_OPENAI_DOMAIN_KEY

### Local Development
- localhost typically works without allowlist for development
- For production, domain allowlist is required

## MCP Tools Available

The MCP server exposes 5 tools:
- `add_task`: Creates new tasks
- `list_tasks`: Lists existing tasks
- `complete_task`: Marks tasks as complete
- `delete_task`: Removes tasks
- `update_task`: Modifies existing tasks

## Database Migrations

Run database migrations before starting the application:

```bash
cd backend/
# Run SQLModel migrations
python -m app.migrations
```

## Testing

### Backend Tests
```bash
cd backend/
pytest
```

### Frontend Tests
```bash
cd frontend/
npm test
```

### MCP Server Tests
```bash
cd mcp-server/
python -m pytest tests/
```

## Troubleshooting

1. **OpenAI ChatKit not loading**: Verify NEXT_PUBLIC_OPENAI_DOMAIN_KEY is set correctly
2. **Database connection errors**: Check DATABASE_URL format in environment files
3. **JWT authentication failures**: Ensure SECRET_KEY is properly set in backend
4. **MCP server not connecting**: Verify OPENAI_API_KEY is set in both backend and MCP server