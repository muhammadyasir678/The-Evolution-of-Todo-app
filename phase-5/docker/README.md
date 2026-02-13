# Docker Configuration for Phase V: Advanced Cloud Deployment

This directory contains Docker configurations for all services in the advanced Todo application with AI chatbot functionality.

## Overview

The Phase V deployment includes:
- Frontend: Next.js application with advanced task management UI
- Backend: FastAPI server with task management and AI integration
- MCP Server: Multi-component protocol server for AI interactions
- Recurring Task Service: Microservice for handling recurring tasks
- Notification Service: Microservice for sending due date reminders
- Audit Service: Microservice for logging all operations
- WebSocket Service: Microservice for real-time synchronization

## Dockerfiles

### Application Services
- `frontend.Dockerfile`: Builds and runs the Next.js frontend application
- `backend.Dockerfile`: Builds and runs the FastAPI backend service
- `mcp-server.Dockerfile`: Builds and runs the MCP server for AI interactions

### Microservices
- `recurring-task-service.Dockerfile`: Builds the recurring task service
- `notification-service.Dockerfile`: Builds the notification service
- `audit-service.Dockerfile`: Builds the audit service
- `websocket-service.Dockerfile`: Builds the WebSocket service

## Docker Compose

The `docker-compose.yml` file defines the complete application stack with all services configured to work together. It includes:

- Frontend and backend services
- MCP server for AI interactions
- All four new microservices (recurring task, notification, audit, websocket)
- Kafka for event streaming
- Zookeeper for Kafka coordination

## Environment Variables

The application requires the following environment variables to be set in a `.env` file:

```bash
DATABASE_URL=postgresql://username:password@neon-host.region.provider.neon.tech/dbname
OPENAI_API_KEY=your_openai_api_key
BETTER_AUTH_SECRET=your_auth_secret
SENDGRID_API_KEY=your_sendgrid_api_key  # For notification service
KAFKA_BROKERS=kafka:9092
```

## Running the Application

1. Make sure you have Docker and Docker Compose installed
2. Set up your environment variables in a `.env` file
3. Run the application with:

```bash
docker-compose up -d
```

4. Access the application at `http://localhost:3000`

## Building Individual Services

To build a specific service:

```bash
# Build frontend
docker build -f frontend.Dockerfile -t todo-frontend:latest ../phase-3/frontend

# Build backend
docker build -f backend.Dockerfile -t todo-backend:latest ../phase-3/backend

# Build MCP server
docker build -f mcp-server.Dockerfile -t todo-mcp-server:latest ../phase-3/mcp-server

# Build recurring task service
docker build -f recurring-task-service.Dockerfile -t recurring-task-service:latest services/recurring-task-service

# Build notification service
docker build -f notification-service.Dockerfile -t notification-service:latest services/notification-service

# Build audit service
docker build -f audit-service.Dockerfile -t audit-service:latest services/audit-service

# Build websocket service
docker build -f websocket-service.Dockerfile -t websocket-service:latest services/websocket-service
```

## Architecture

This Phase V implementation features:
- Event-driven architecture using Kafka for communication between services
- Dapr for standardized microservice patterns (pub/sub, state management, etc.)
- Real-time synchronization using WebSocket connections
- Advanced task features: recurring tasks, due date reminders, priority management, tagging
- Cloud-native deployment patterns with containerization