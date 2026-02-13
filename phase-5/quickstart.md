# Quickstart Guide: Advanced Cloud Deployment

## Overview

This guide provides step-by-step instructions for deploying the Todo application with advanced features (recurring tasks, due date reminders, priority management, tagging, real-time sync) to a local Kubernetes cluster using Minikube.

## Prerequisites

### System Requirements
- Operating System: Linux, macOS, or Windows
- RAM: Minimum 8GB recommended (16GB preferred)
- Disk Space: 20GB free space
- CPU: Multi-core processor

### Required Software
1. **Docker** (version 20.10 or higher)
   ```bash
   docker --version
   ```

2. **kubectl** (Kubernetes CLI)
   ```bash
   kubectl version --client
   ```

3. **Helm** (version 3.x)
   ```bash
   helm version
   ```

4. **Minikube** (latest version)
   ```bash
   minikube version
   ```

5. **Dapr CLI**
   ```bash
   dapr --version
   ```

6. **Kafka client tools** (optional, for debugging)
   ```bash
   kafka-topics.sh --version  # if Kafka is installed locally
   ```

### Optional AI Development Tools
- Docker AI (Gordon) - for Dockerfile generation
- kubectl-ai - for Kubernetes manifest assistance
- kagent - for cluster troubleshooting

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd The-Evolution-of-Todo-app
cd phase-5
```

### 2. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources
minikube start --memory=8192 --cpus=4

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. Install Dapr
```bash
# Initialize Dapr in Kubernetes mode
dapr init -k

# Verify Dapr is running
dapr status -k
```

## Deployment Steps

### 1. Deploy Kafka to Minikube
```bash
# Create Kafka namespace
kubectl create namespace kafka

# Install Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for the operator to be ready
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy Kafka cluster and topics
kubectl apply -f k8s/kafka/strimzi-kafka.yaml

# Wait for Kafka cluster to be ready
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

### 2. Apply Dapr Components
```bash
# Apply Dapr component configurations
kubectl apply -f k8s/dapr/pubsub.yaml
kubectl apply -f k8s/dapr/statestore.yaml
kubectl apply -f k8s/dapr/secretstore.yaml
```

### 3. Configure Docker Environment for Minikube
```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 4. Build Docker Images
```bash
# Build frontend image
docker build -t todo-frontend:latest -f ../phase-3/frontend/Dockerfile ../phase-3/frontend

# Build backend image
docker build -t todo-backend:latest -f ../phase-3/backend/Dockerfile ../phase-3/backend

# Build MCP server image
docker build -t todo-mcp-server:latest -f ../phase-3/mcp-server/Dockerfile ../phase-3/mcp-server

# Build recurring task service image
docker build -t recurring-task-service:latest -f services/recurring-task-service/Dockerfile services/recurring-task-service

# Build notification service image
docker build -t notification-service:latest -f services/notification-service/Dockerfile services/notification-service

# Build audit service image
docker build -t audit-service:latest -f services/audit-service/Dockerfile services/audit-service

# Build websocket service image
docker build -t websocket-service:latest -f services/websocket-service/Dockerfile services/websocket-service

# Verify images were built
docker images | grep -E "(todo-frontend|todo-backend|todo-mcp-server|recurring-task-service|notification-service|audit-service|websocket-service)"
```

### 5. Deploy Application to Minikube
```bash
# Create secrets for the application
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://username:password@neon-host.region.provider.neon.tech/dbname" \
  --from-literal=OPENAI_API_KEY="your_openai_api_key" \
  --from-literal=BETTER_AUTH_SECRET="your_auth_secret" \
  --from-literal=SENDGRID_API_KEY="your_sendgrid_api_key" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy using Helm
helm upgrade --install todo-app-v5 helm-charts/todo-app-v5 --namespace todo-app --create-namespace

# Wait for all deployments to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=recurring-task-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=notification-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=audit-service -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=websocket-service -n todo-app --timeout=300s
```

## Accessing the Application

### Method 1: Using Minikube Service
```bash
# Get the frontend service URL
minikube service frontend-service -n todo-app --url
```

### Method 2: Using Port Forwarding
```bash
# Forward the frontend service port
kubectl port-forward svc/frontend-service 3000:80 -n todo-app
```

## Testing the Advanced Features

### 1. Recurring Tasks
1. Create a task with a recurrence pattern (daily, weekly, or monthly)
2. Complete the task
3. Verify that the system automatically creates the next occurrence

### 2. Due Date Reminders
1. Create a task with a due date and reminder time
2. Check that a reminder event is published to the reminders topic
3. Verify that the notification service processes the reminder

### 3. Priority and Tags
1. Create tasks with different priorities (high, medium, low)
2. Add tags to tasks
3. Use the filtering UI to filter by priority and tags

### 4. Real-Time Sync
1. Open the application in multiple browser windows/tabs
2. Create or update a task in one window
3. Verify that the change appears in real-time in other windows

### 5. Event-Driven Flows
1. Create a task and verify an event is published to the task-events topic
2. Complete a recurring task and verify the next occurrence is created
3. Check the audit service logs for audit entries

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods -n todo-app
# Expected: All pods in Running state
```

### 2. Check Service Connectivity
```bash
# Check all services are available
kubectl get services -n todo-app

# Test internal connectivity between services
kubectl exec -it deployment/backend -n todo-app -- curl -v http://recurring-task-service:8001/health
kubectl exec -it deployment/backend -n todo-app -- curl -v http://notification-service:8002/health
kubectl exec -it deployment/backend -n todo-app -- curl -v http://audit-service:8003/health
kubectl exec -it deployment/backend -n todo-app -- curl -v http://websocket-service:8004/health
```

### 3. Verify Kafka Topics
```bash
# Check Kafka topics exist and have messages
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Check messages in task-events topic
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic task-events --from-beginning --max-messages 5
```

### 4. Check Application Functionality
1. Open your browser to the frontend URL obtained earlier
2. Verify the UI loads properly
3. Test creating, updating, and completing tasks
4. Verify all advanced features (priority, tags, due dates, recurrence) work correctly
5. Check that real-time sync works across multiple browser instances

### 5. Check Logs
```bash
# View frontend logs
kubectl logs deployment/frontend -n todo-app

# View backend logs
kubectl logs deployment/backend -n todo-app

# View MCP server logs
kubectl logs deployment/mcp-server -n todo-app

# View recurring task service logs
kubectl logs deployment/recurring-task-service -n todo-app

# View notification service logs
kubectl logs deployment/notification-service -n todo-app

# View audit service logs
kubectl logs deployment/audit-service -n todo-app

# View websocket service logs
kubectl logs deployment/websocket-service -n todo-app
```

## Troubleshooting Guide

### Issue: Images Not Found
**Symptom**: `ImagePullBackOff` error
**Solution**: Ensure you ran `eval $(minikube docker-env)` before building images

### Issue: Database Connection Failure
**Symptom**: Backend pods crash with database connection errors
**Solution**: Verify DATABASE_URL in secrets and network connectivity to Neon

### Issue: Service Not Accessible
**Symptom**: Cannot access frontend via NodePort
**Solution**: Check service type is NodePort and firewall settings

### Issue: Insufficient Resources
**Symptom**: Pods stuck in Pending state
**Solution**: Increase Minikube resources or reduce resource requests in values.yaml

### Issue: Kafka Connection Problems
**Symptom**: Services can't connect to Kafka
**Solution**: 
```bash
# Check Kafka pods
kubectl get pods -n kafka

# Check Kafka endpoints
kubectl get svc -n kafka

# Check Kafka logs
kubectl logs -f deployment/my-cluster-kafka -n kafka
```

### Issue: Dapr Sidecar Problems
**Symptom**: Services can't publish/subscribe to Kafka via Dapr
**Solution**:
```bash
# Check Dapr status
dapr status -k

# Check Dapr logs
kubectl logs -f deployment/dapr-placement-server -n dapr-system
```

## Cleanup

### To Uninstall the Application
```bash
# Remove Helm release
helm uninstall todo-app-v5 -n todo-app

# Remove namespace
kubectl delete namespace todo-app

# Remove Kafka
kubectl delete -f k8s/kafka/strimzi-kafka.yaml
kubectl delete -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl delete namespace kafka

# Remove Dapr components
kubectl delete -f k8s/dapr/pubsub.yaml
kubectl delete -f k8s/dapr/statestore.yaml
kubectl delete -f k8s/dapr/secretstore.yaml

# Remove Docker images (optional)
docker rmi todo-frontend:latest todo-backend:latest todo-mcp-server:latest \
        recurring-task-service:latest notification-service:latest \
        audit-service:latest websocket-service:latest
```

### To Stop Minikube
```bash
minikube stop
```

### To Delete Minikube Cluster
```bash
minikube delete
```

## Next Steps

1. **Customize Configuration**: Modify `helm-charts/todo-app-v5/values.yaml` to adjust resource limits, replica counts, and other parameters
2. **Add Monitoring**: Deploy Prometheus and Grafana for metrics
3. **Configure Ingress**: Set up proper domain routing using Kubernetes Ingress
4. **Production Preparation**: Adjust security settings, enable TLS, and set up proper logging