# Quickstart Guide: Kubernetes Minikube Deployment

## Overview

This guide provides step-by-step instructions for deploying the Todo application with AI chatbot functionality to a local Kubernetes cluster using Minikube. The deployment includes containerized frontend, backend, and MCP server components.

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

### Optional AI Development Tools
- Docker AI (Gordon) - for Dockerfile generation
- kubectl-ai - for Kubernetes manifest assistance
- kagent - for cluster troubleshooting

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd The-Evolution-of-Todo-app
cd phase-4
```

### 2. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources
minikube start --memory=8192 --cpus=4

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. Configure Docker Environment for Minikube
```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 4. Prepare Environment Variables
Create a `.env` file with your configuration:
```bash
# Example .env file
DATABASE_URL=your_neon_postgres_connection_string
OPENAI_API_KEY=your_openai_api_key
BETTER_AUTH_SECRET=your_auth_secret
```

## Deployment Steps

### 1. Build Docker Images
```bash
# Run the build script to build all images in Minikube environment
./scripts/build-images.sh
```

### 2. Deploy Using Helm
```bash
# Run the deployment script
./scripts/deploy-minikube.sh
```

### 3. Verify Deployment
```bash
# Check all pods are running
kubectl get pods -n todo-app

# Check all services are available
kubectl get services -n todo-app

# Check deployment status
kubectl get deployments -n todo-app
```

## Accessing the Application

### Method 1: Using Minikube Service
```bash
# Get the frontend service URL
minikube service frontend-service -n todo-app --url
```

### Method 2: Using NodePort
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Access frontend via NodePort (default 30000)
echo "Frontend: http://$MINIKUBE_IP:30000"
```

## AI-Assisted Development Commands

### Docker AI (Gordon) Commands
```bash
# Generate optimized Dockerfile for Next.js
docker ai "Create optimized Dockerfile for Next.js production app"

# Optimize existing Dockerfile
docker ai "Reduce todo-frontend image size"
```

### kubectl-ai Commands
```bash
# Deploy frontend with specific configuration
kubectl-ai "deploy todo frontend with 3 replicas in todo-app namespace"

# Scale backend service
kubectl-ai "scale backend-deployment to 3 replicas in todo-app namespace"

# Troubleshoot failing pods
kubectl-ai "check why pods are failing in todo-app namespace"
```

### kagent Commands
```bash
# Analyze cluster health
kagent "analyze health of todo-app namespace"

# Troubleshoot deployment issues
kagent "why is my backend pod crashing in todo-app?"

# Optimize resource allocation
kagent "optimize resource allocation for todo-app deployment"
```

## Local Development with Docker Compose

For rapid development cycles, you can also use Docker Compose:

```bash
# Navigate to docker directory
cd docker/

# Start services with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods -n todo-app
# Expected: All pods in Running state
```

### 2. Check Service Connectivity
```bash
# Test internal connectivity
kubectl exec -it deployment/backend -n todo-app -- curl -v http://mcp-service:8080/health
kubectl exec -it deployment/frontend -n todo-app -- curl -v http://backend-service:8000/health
```

### 3. Verify Application Functionality
1. Open your browser to the frontend URL obtained earlier
2. Verify the UI loads properly
3. Test the chatbot functionality
4. Ensure database connections work properly

### 4. Check Logs
```bash
# View frontend logs
kubectl logs deployment/frontend -n todo-app

# View backend logs
kubectl logs deployment/backend -n todo-app

# View MCP server logs
kubectl logs deployment/mcp-server -n todo-app
```

## Common Issues and Solutions

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

## Cleanup

### To Uninstall the Application
```bash
# Remove Helm release
helm uninstall todo-app -n todo-app

# Remove namespace
kubectl delete namespace todo-app

# Remove Docker images (optional)
docker rmi todo-frontend:latest todo-backend:latest todo-mcp-server:latest
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

1. **Customize Configuration**: Modify `helm-charts/todo-app/values.yaml` to adjust resource limits, replica counts, and other parameters
2. **Add Monitoring**: Deploy Prometheus and Grafana for metrics
3. **Configure Ingress**: Set up proper domain routing using Kubernetes Ingress
4. **Production Preparation**: Adjust security settings, enable TLS, and set up proper logging