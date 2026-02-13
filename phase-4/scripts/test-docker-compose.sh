#!/bin/bash

# Task ID: T329
# Test Docker Compose locally with .env file and full functionality verification

set -e  # Exit immediately if a command exits with a non-zero status

echo "Testing Docker Compose locally with full functionality verification..."

# Create a sample .env file if it doesn't exist
ENV_FILE="phase-4/docker/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating sample .env file for local testing..."
    cat > "$ENV_FILE" << EOF
# Sample environment variables for local Docker Compose testing
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
OPENAI_API_KEY=sk-sample-key-for-local-testing
BETTER_AUTH_SECRET=local-auth-secret-for-testing
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo "Sample .env file created at $ENV_FILE"
fi

# Start the services using Docker Compose
echo "Starting services with Docker Compose..."
cd phase-4/docker
docker-compose up -d

# Wait a moment for services to start
sleep 10

# Check if all services are running
echo "Checking if all services are running..."
docker-compose ps

# Test frontend accessibility
echo "Testing frontend accessibility..."
if curl -f http://localhost:3000/ 2>/dev/null; then
    echo "✓ Frontend is accessible"
else
    echo "✗ Frontend is not accessible"
fi

# Test backend API
echo "Testing backend API..."
if curl -f http://localhost:8000/health 2>/dev/null; then
    echo "✓ Backend API is accessible"
else
    echo "✗ Backend API is not accessible"
fi

# Test MCP server
echo "Testing MCP server..."
if curl -f http://localhost:8080/health 2>/dev/null; then
    echo "✓ MCP server is accessible"
else
    echo "✗ MCP server is not accessible"
fi

# Run basic functionality tests
echo "Running basic functionality tests..."

# Test creating a task
echo "Testing task creation..."
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/test-user/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task from Docker Compose test", "description":"This is a test task created during Docker Compose verification"}')

if [[ $TASK_RESPONSE == *"id"* ]]; then
    echo "✓ Task creation successful"
    TASK_ID=$(echo $TASK_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)
    echo "Created task with ID: $TASK_ID"
else
    echo "✗ Task creation failed"
    echo "Response: $TASK_RESPONSE"
fi

# Test getting tasks
echo "Testing task retrieval..."
TASKS_RESPONSE=$(curl -s http://localhost:8000/api/test-user/tasks)
if [[ $TASKS_RESPONSE == *"[{"* ]] || [[ $TASKS_RESPONSE == *"[]"* ]]; then
    echo "✓ Task retrieval successful"
else
    echo "✗ Task retrieval failed"
    echo "Response: $TASKS_RESPONSE"
fi

# Test updating a task
if [ ! -z "$TASK_ID" ]; then
    echo "Testing task update..."
    UPDATE_RESPONSE=$(curl -s -X PUT http://localhost:8000/api/test-user/tasks/$TASK_ID \
      -H "Content-Type: application/json" \
      -d '{"title":"Updated test task", "completed":true}')
    
    if [[ $UPDATE_RESPONSE == *"$TASK_ID"* ]]; then
        echo "✓ Task update successful"
    else
        echo "✗ Task update failed"
        echo "Response: $UPDATE_RESPONSE"
    fi
fi

# Check logs for any errors
echo "Checking service logs for errors..."
echo "=== Frontend logs ==="
docker-compose logs frontend | tail -20
echo "=== Backend logs ==="
docker-compose logs backend | tail -20
echo "=== MCP server logs ==="
docker-compose logs mcp-server | tail -20

echo "Docker Compose functionality test completed!"
echo "Stopping services..."
docker-compose down