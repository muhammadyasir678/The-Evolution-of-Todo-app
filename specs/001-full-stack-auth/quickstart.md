# Quickstart Guide: Full-Stack Web Application with Authentication

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL (can use Neon Serverless)
- Git

## Setup Instructions

### 1. Clone and Navigate
```bash
cd phase-2
```

### 2. Setup Frontend (Next.js)
```bash
# Create frontend directory
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir

# Navigate to frontend and install dependencies
cd frontend
npm install better-auth react-icons
```

### 3. Setup Backend (FastAPI)
```bash
# Create backend directory
cd ../backend
uv init
uv add fastapi sqlmodel psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart uvicorn better-auth
```

### 4. Environment Configuration

#### Frontend (.env.local)
```env
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-min-length-of-32-characters
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-min-length-of-32-characters
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### 5. Database Setup (Neon)
1. Create a Neon account and project
2. Copy the connection string
3. Update DATABASE_URL in both frontend and backend .env files

### 6. Run Applications

#### Start Backend
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

#### Start Frontend
```bash
cd frontend
npm run dev
```

## Key Features

### Authentication Flow
- Users can sign up with email/password
- Users can sign in with email/password
- JWT tokens are automatically managed by Better Auth
- Protected routes redirect unauthenticated users to sign-in

### Task Management
- Create tasks with title (1-200 chars) and optional description (max 1000 chars)
- View all tasks in a responsive list
- Update task title and description
- Mark tasks as complete/incomplete
- Delete tasks with confirmation modal

### Data Isolation
- Each user sees only their own tasks
- Backend enforces user-specific data filtering
- JWT token validation ensures proper access control

## Project Structure
```
phase-2/
├── frontend/              # Next.js 16+ App Router
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── (protected)/
│   │   │   └── tasks/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   └── Header.tsx
│   ├── lib/
│   │   ├── auth.ts       # Better Auth config
│   │   ├── api.ts        # API client
│   │   └── types.ts
│   ├── public/
│   ├── .env.local
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── package.json
└── backend/               # Python FastAPI
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models.py
    │   ├── database.py
    │   ├── auth.py
    │   └── routes/
    │       ├── __init__.py
    │       └── tasks.py
    ├── tests/
    ├── alembic/           # migrations
    ├── .env
    ├── pyproject.toml
    └── README.md
```

## API Endpoints
- GET    /api/{user_id}/tasks              - List all user's tasks
- POST   /api/{user_id}/tasks              - Create new task
- GET    /api/{user_id}/tasks/{task_id}    - Get task details
- PUT    /api/{user_id}/tasks/{task_id}    - Update task
- DELETE /api/{user_id}/tasks/{task_id}    - Delete task
- PATCH  /api/{user_id}/tasks/{task_id}/complete - Toggle completion

## Testing
- Frontend: Manual testing in browser
- Backend: Unit tests with pytest
- End-to-end: Test auth flows and CRUD operations

## Deployment
- Frontend: Deploy to Vercel (connected to GitHub repo)
- Backend: Deploy to Render/Railway/Fly.io
- Database: Neon Serverless