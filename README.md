# Todo Application - Full-Stack Web Application

This is a full-stack web application with user authentication and task management functionality. The system consists of a Next.js frontend with Better Auth integration and a FastAPI backend with JWT authentication, connected to a Neon Serverless PostgreSQL database. The application provides secure, isolated task management for each authenticated user with responsive UI design.

## Phases of Development

- **Phase I**: Console Todo Application with in-memory data structures
- **Phase II**: Full Stack Todo App with Authentication and user isolation
- **Phase III**: AI-Powered Todo Chatbot with natural language interaction
- **Phase IV**: Advanced Cloud Deployment with event-driven architecture

## Current Features (Phase III)

- User registration and authentication
- Secure task management with user isolation
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Natural language task management via AI assistant
- Conversation history persistence
- Responsive design for mobile and desktop
- Proper error handling and validation

## Architecture

- **Frontend**: Next.js 16+ with App Router, Tailwind CSS, Better Auth
- **Backend**: FastAPI with Python 3.13+, SQLModel ORM
- **AI Component**: OpenAI Agents SDK with MCP tools
- **MCP Server**: Dedicated server for AI tool integration
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens

## Setup

### Prerequisites

- Node.js 18+ for frontend
- Python 3.13+ for backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```
Or with pip:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@host:port/database
BETTER_AUTH_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

4. Initialize the database:
```bash
python -c "from app.database import engine, create_db_and_tables; create_db_and_tables()"
```

5. Run the backend:
```bash
python app/main.py
```
Or with uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

4. Run the development server:
```bash
npm run dev
```

## Running the Application

### Phase III Setup

1. Start the MCP server:
```bash
cd phase-3/mcp-server/
uv run src/server.py
```

2. Start the backend server on port 8000:
```bash
cd phase-3/backend/
uvicorn app.main:app --reload --port 8000
```

3. Start the frontend server on port 3000:
```bash
cd phase-3/frontend/
npm run dev
```

4. Access the application at http://localhost:3000 and navigate to the chat interface

### Phase II Setup (Previous phases)
1. Start the backend server on port 8000
2. Start the frontend server on port 3000
3. Access the application at http://localhost:3000