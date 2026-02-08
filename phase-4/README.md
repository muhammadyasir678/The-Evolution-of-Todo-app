# Phase 4: Kubernetes Minikube Deployment

This directory contains all files related to the Kubernetes deployment of the Todo application with AI chatbot functionality.

## Overview

This phase focuses on containerizing and deploying the Phase III chatbot application on local Kubernetes using Minikube. The implementation includes:

- Dockerfiles for frontend, backend, and MCP server with multi-stage builds
- Kubernetes manifests for deployments and services
- Helm chart for simplified deployment
- Scripts for building images and deploying to Minikube
- Documentation for the deployment process

## Prerequisites

- Docker (version 20.10 or higher)
- kubectl (Kubernetes CLI)
- Helm (version 3.x)
- Minikube (latest version)
- At least 8GB of RAM recommended

## Directory Structure

- `docker/` - Dockerfiles and docker-compose configuration
- `k8s/` - Kubernetes manifests for deployments, services, configmaps, and secrets
- `helm-charts/` - Helm chart packaging the entire application
- `scripts/` - Utility scripts for building and deployment

## Build Instructions

### 1. Setup Minikube Environment

```bash
# Start Minikube with sufficient resources
minikube start --memory=8192 --cpus=4

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Set Docker Environment to Use Minikube

```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 3. Build Docker Images

```bash
# Run the build script to build all images in Minikube environment
./scripts/build-images.sh
```

## Deployment Instructions

### 1. Prepare Environment Variables

Create a `.env` file with your configuration:

```bash
# Example .env file
DATABASE_URL=your_neon_postgres_connection_string
OPENAI_API_KEY=your_openai_api_key
BETTER_AUTH_SECRET=your_auth_secret
```

### 2. Deploy Using Helm

```bash
# Run the deployment script
./scripts/deploy-minikube.sh
```

### 3. Access the Application

```bash
# Get the frontend service URL
minikube service frontend-service -n todo-app --url
```

Or access via NodePort:

```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Access frontend via NodePort (default 30000)
echo "Frontend: http://$MINIKUBE_IP:30000"
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

## AI DevOps Commands Used

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