#!/bin/bash

# Script to deploy Phase V services to Minikube
# This script builds Docker images in Minikube environment and deploys the full stack

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment to Minikube..."

# Set Docker environment to use Minikube's Docker daemon
echo "Setting Docker environment to use Minikube..."
eval $(minikube docker-env)

# Build Docker images in Minikube environment
echo "Building frontend Docker image..."
docker build -t todo-frontend:latest -f ../phase-3/frontend/Dockerfile ../phase-3/frontend

echo "Building backend Docker image..."
docker build -t todo-backend:latest -f ../phase-3/backend/Dockerfile ../phase-3/backend

echo "Building MCP server Docker image..."
docker build -t todo-mcp-server:latest -f ../phase-3/mcp-server/Dockerfile ../phase-3/mcp-server

echo "Building recurring-task-service Docker image..."
docker build -t recurring-task-service:latest -f services/recurring-task-service/Dockerfile services/recurring-task-service

echo "Building notification-service Docker image..."
docker build -t notification-service:latest -f services/notification-service/Dockerfile services/notification-service

echo "Building audit-service Docker image..."
docker build -t audit-service:latest -f services/audit-service/Dockerfile services/audit-service

echo "Building websocket-service Docker image..."
docker build -t websocket-service:latest -f services/websocket-service/Dockerfile services/websocket-service

echo "Verifying images were built..."
docker images | grep -E "(todo-frontend|todo-backend|todo-mcp-server|recurring-task-service|notification-service|audit-service|websocket-service)"

# Create namespace if it doesn't exist
echo "Creating todo-app namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka using Redpanda
echo "Deploying Kafka with Redpanda..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f k8s/kafka/redpanda-kafka.yaml

echo "Waiting for Redpanda cluster to be ready..."
kubectl wait --for=condition=ready pod -l app=redpanda-single -n kafka --timeout=300s

# Deploy Dapr
echo "Installing Dapr..."
dapr init -k

# Apply Dapr components
echo "Applying Dapr components..."
kubectl apply -f k8s/dapr/config.yaml
kubectl apply -f k8s/dapr/pubsub.yaml  # Local Kafka configuration
kubectl apply -f k8s/dapr/statestore.yaml
kubectl apply -f k8s/dapr/secretstore.yaml
kubectl apply -f k8s/dapr/bindings.cron.yaml
kubectl apply -f k8s/dapr/reminder-cron-binding.yaml
kubectl apply -f k8s/dapr/backend-reminder-subscription.yaml

# Create secrets for the application
echo "Creating application secrets..."
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="${DATABASE_URL:-postgresql://username:password@neon-host.region.provider.neon.tech/dbname}" \
  --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY:-your_openai_api_key}" \
  --from-literal=BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET:-your_auth_secret}" \
  --from-literal=SENDGRID_API_KEY="${SENDGRID_API_KEY:-your_sendgrid_api_key}" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy the application using Helm
echo "Deploying application with Helm..."
helm upgrade --install todo-app-v5 helm-charts/todo-app-v5 --namespace todo-app --create-namespace

# Wait for all deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=recurring-task-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=notification-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=audit-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=websocket-service -n todo-app --timeout=300s

# Display deployment status
echo "Displaying pods..."
kubectl get pods -n todo-app

echo "Displaying services..."
kubectl get services -n todo-app

echo "Displaying deployments..."
kubectl get deployments -n todo-app

echo "Deployment to Minikube completed successfully!"
echo "Access the frontend at: $(minikube service frontend-service -n todo-app --url)"