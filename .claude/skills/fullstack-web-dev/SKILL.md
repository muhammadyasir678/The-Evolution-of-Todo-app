---
name: fullstack-web-dev
description: Build modern fullstack web applications using Next.js and FastAPI with clean architecture. Use for scalable production-ready web systems.
---

# Fullstack Web Development

## Instructions

1. **Frontend (Next.js 16+)**
   - Use App Router (`app/` directory)
   - Server Components by default
   - Client Components only when required
   - Implement routing, layouts, and loading states
   - Use Tailwind CSS for styling
   - Ensure responsive, mobile-first design

2. **Backend (FastAPI)**
   - Build RESTful APIs using proper HTTP methods (GET, POST, PUT, DELETE)
   - Structure backend with routers, services, and models
   - Use SQLModel ORM for database interactions
   - Implement dependency injection for database sessions
   - Return standardized API responses and status codes

3. **Database Layer**
   - Define SQLModel models with clear relationships
   - Use migrations-friendly schema design
   - Separate data models and schemas when needed
   - Handle CRUD operations cleanly

4. **Authentication & Security**
   - Integrate Better Auth with JWT-based authentication
   - Protect routes using auth dependencies
   - Handle token issuance, refresh, and validation
   - Secure environment variables and secrets

5. **Monorepo Management**
   - Maintain clear separation between `frontend/` and `backend/`
   - Share types or contracts where applicable
   - Use consistent naming and folder conventions
   - Support independent deployment of frontend and backend

## Best Practices

- Follow clean code and separation of concerns
- Keep API contracts explicit and documented
- Use type safety on both frontend and backend
- Validate user input on server side
- Handle errors gracefully with meaningful messages
- Optimize for performance and scalability
- Follow REST standards and HTTP semantics
- Write reusable components and services

## Example Structure

```text
root/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   ├── components/
│   ├── lib/
│   └── tailwind.config.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── services/
│   │   └── core/
│   └── pyproject.toml
│
└── README.md
