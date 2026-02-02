# Todo App - Full-Stack Web Application

A full-stack web application with user authentication and task management functionality built with Next.js and FastAPI.

## Features

- User authentication (sign up/sign in)
- Task management (create, read, update, delete, mark complete)
- User-specific data isolation
- Responsive UI with Tailwind CSS
- JWT-based authentication

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth
- **Styling**: Tailwind CSS

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
    ├── .env
    ├── pyproject.toml
    └── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or access to Neon Serverless)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd phase-2/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.local.example .env.local
```

4. Update environment variables in `.env.local`:
```
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-min-length-of-32-characters
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Start the development server:
```bash
npm run dev
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd phase-2/backend
```

2. Set up Python virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install poetry
poetry install
```

Or if using pip:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Update environment variables in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-token-with-min-length-of-32-characters
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

6. Start the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

All endpoints require JWT token authentication via Authorization header:
```
Authorization: Bearer <jwt_token>
```

- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get task details
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Security

- JWT-based authentication
- User-specific data filtering
- Input validation and sanitization
- Secure password handling via Better Auth
- CORS configured for frontend-backend communication

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Configure environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Render/Railway/Fly.io)
1. Create a new service
2. Configure environment variables
3. Set up PostgreSQL database (Neon recommended)
4. Deploy the FastAPI application

## Development

- Frontend runs on http://localhost:3000
- Backend runs on http://localhost:8000
- API endpoints follow the pattern: http://localhost:8000/api/{user_id}/...

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.