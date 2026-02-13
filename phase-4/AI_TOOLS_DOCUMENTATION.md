# AI-Assisted Development Tools Documentation

## Docker AI (Gordon) Commands

The following Docker AI commands can be used for optimizing Dockerfiles:

```bash
# Optimize frontend Dockerfile
docker ai "optimize the multi-stage build in frontend.Dockerfile for smaller image size"

# Optimize backend Dockerfile
docker ai "reduce the size of the backend Docker image by optimizing layer caching"

# General Dockerfile improvements
docker ai "add security best practices to all Dockerfiles"
```

## kubectl-ai Commands

The following kubectl-ai commands can assist with Kubernetes operations:

```bash
# Deploy frontend with specific configuration
kubectl-ai "deploy todo frontend with 3 replicas in todo-app namespace"

# Scale backend service
kubectl-ai "scale backend-deployment to 3 replicas in todo-app namespace"

# Check failing pods
kubectl-ai "check why pods are failing in todo-app namespace"

# Get status of all resources
kubectl-ai "show status of all deployments and services in todo-app namespace"

# Create a new deployment
kubectl-ai "create a deployment for a new service called analytics-service"
```

## kagent Commands

The following kagent commands can help with cluster management and troubleshooting:

```bash
# Analyze cluster health
kagent "analyze health of todo-app namespace"

# Troubleshoot deployment issues
kagent "why is my backend pod crashing in todo-app?"

# Optimize resource allocation
kagent "optimize resource allocation for todo-app deployment"

# Check logs and suggest fixes
kagent "review logs from all pods and identify potential issues"
```

## Integration into Deployment Workflow

### In build-images.sh
```bash
# Use Gordon to optimize Dockerfiles before building
docker ai "optimize Dockerfile at phase-5/docker/frontend.Dockerfile"
docker ai "optimize Dockerfile at phase-5/docker/backend.Dockerfile"
docker ai "optimize Dockerfile at phase-5/docker/mcp-server.Dockerfile"
```

### In deploy scripts
```bash
# Use kubectl-ai to verify deployment status
kubectl-ai "check if all pods are running in todo-app namespace"

# Use kagent for troubleshooting
kagent "analyze health of all deployments in todo-app namespace"
```

## Summary

These AI-assisted tools can significantly speed up development and operational tasks:
- Docker AI (Gordon) helps optimize container builds
- kubectl-ai assists with Kubernetes resource management
- kagent provides intelligent troubleshooting capabilities