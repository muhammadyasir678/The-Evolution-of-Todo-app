---
id: 0003
title: k8s-minikube-deployment-tasks
stage: tasks
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-k8s-minikube-deployment
branch: 001-k8s-minikube-deployment
user: unknown
command: /sp.tasks
labels: ["kubernetes", "docker", "helm", "minikube", "deployment", "containerization", "tasks"]
links:
  spec: ../specs/001-k8s-minikube-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-k8s-minikube-deployment/tasks.md
tests:
  - none
---

## Prompt

/sp.tasks

PHASE: Phase IV - Local Kubernetes Deployment (Minikube)

BASE: Approved speckit.plan for Phase IV

TASKS:

T-301: Create Project Structure
- Create phase-4/ directory
- Create subdirectories: docker/, k8s/, helm-charts/, scripts/
- Create README.md and CLAUDE.md placeholders
- Reference: speckit.plan §Project Structure

T-302: Create Frontend Dockerfile
- Create docker/frontend.Dockerfile
- Implement multi-stage build (builder + production)
- Stage 1: Install dependencies and build Next.js
- Stage 2: Copy build artifacts, production dependencies only
- Expose port 3000
- Add health check
- Optimize for smaller image size
- Reference: speckit.plan §Frontend Dockerfile

T-303: Create Backend Dockerfile
- Create docker/backend.Dockerfile
- Implement multi-stage build (builder + production)
- Stage 1: Install Python dependencies with uv
- Stage 2: Copy dependencies and application code
- Expose port 8000
- Add health check endpoint
- Optimize for smaller image size
- Reference: speckit.plan §Backend Dockerfile

T-304: Create MCP Server Dockerfile
- Create docker/mcp-server.Dockerfile
- Install Python dependencies with uv
- Copy MCP server code
- Configure entry point
- Reference: speckit.plan §MCP Server Dockerfile

T-305: Create Docker Compose File
- Create docker/docker-compose.yml
- Define services: frontend, backend, mcp-server
- Configure service dependencies
- Set environment variables from .env
- Map ports for local access
- Reference: speckit.plan §docker-compose.yml

T-306: Test Docker Compose Locally
- Create .env file with required variables
- Run: docker-compose -f docker/docker-compose.yml up
- Verify all services start without errors
- Test frontend accessible at localhost:3000
- Test backend API at localhost:8000
- Test full chat functionality
- Reference: speckit.plan §Docker Testing

T-307: Create Kubernetes Namespace Manifest
- Create k8s/namespace.yaml
- Define namespace: todo-app
- Reference: speckit.plan §Namespace

T-308: Create Kubernetes ConfigMap
- Create k8s/configmap.yaml
- Add non-sensitive configuration
- Include: NEXT_PUBLIC_API_URL, ports
- Reference: speckit.plan §ConfigMap

T-309: Create Kubernetes Secret Manifest
- Create k8s/secret.yaml (template only, values separate)
- Define secret: todo-secrets
- Keys: DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET
- Document base64 encoding requirement
- Reference: speckit.plan §Secret

T-310: Create Frontend Kubernetes Deployment
- Create k8s/frontend-deployment.yaml
- Define Deployment with 2 replicas
- Configure container with image, port, env from ConfigMap/Secret
- Add resource requests and limits
- Add readiness and liveness probes
- Reference: speckit.plan §Frontend Deployment

T-311: Create Frontend Kubernetes Service
- Create k8s/frontend-service.yaml
- Define Service type: NodePort
- NodePort: 30000
- Selector matches frontend pods
- Reference: speckit.plan §Services

T-312: Create Backend Kubernetes Deployment
- Create k8s/backend-deployment.yaml
- Define Deployment with 2 replicas
- Configure container with image, port, env from ConfigMap/Secret
- Add resource requests and limits
- Add readiness and liveness probes (HTTP /health)
- Reference: speckit.plan §Backend Deployment

T-313: Create Backend Kubernetes Service
- Create k8s/backend-service.yaml
- Define Service type: ClusterIP
- Port: 8000
- Selector matches backend pods
- Reference: speckit.plan §Services

T-314: Create MCP Server Kubernetes Deployment
- Create k8s/mcp-deployment.yaml
- Define Deployment with 1 replica
- Configure container with image, env from Secret
- Add resource requests and limits
- Reference: speckit.plan §MCP Server Deployment

T-315: Create MCP Server Kubernetes Service
- Create k8s/mcp-service.yaml
- Define Service type: ClusterIP
- Selector matches MCP pods
- Reference: speckit.plan §Services

T-316: Create Helm Chart Structure
- Create helm-charts/todo-app/ directory
- Create Chart.yaml with metadata
- Create values.yaml with parameters
- Create templates/ directory
- Reference: speckit.plan §Helm Chart Structure

T-317: Create Helm Chart Templates
- Copy all k8s/*.yaml to templates/
- Parameterize with {{ .Values.* }} syntax
- Support replicas, image tags, resources from values.yaml
- Create _helpers.tpl for reusable template functions
- Reference: speckit.plan §Templates

T-318: Create Build Script
- Create scripts/build-images.sh
- Set Minikube Docker environment
- Build all three images (frontend, backend, mcp-server)
- Tag images appropriately
- Make script executable
- Reference: speckit.plan §Build Images

T-319: Create Deployment Script
- Create scripts/deploy-minikube.sh
- Create namespace if not exists
- Create secrets from environment variables
- Install Helm chart with values
- Display deployment status
- Show access instructions
- Make script executable
- Reference: speckit.plan §Deploy with Helm

T-320: Setup Minikube Environment
- Document Minikube installation steps
- Start Minikube cluster
- Enable necessary addons (ingress if needed)
- Verify cluster is running
- Reference: speckit.plan §Setup

T-321: Build Docker Images in Minikube
- Set Minikube Docker environment: eval $(minikube docker-env)
- Run build-images.sh script
- Verify images created: docker images | grep todo
- Reference: speckit.plan §Build Images

T-322: Deploy Application to Minikube
- Create Kubernetes secrets manually with actual values
- Run deploy-minikube.sh script
- Wait for all pods to be Running
- Check pod status: kubectl get pods -n todo-app
- Reference: speckit.plan §Deploy with Helm

T-323: Test Application on Minikube
- Get Minikube IP: minikube ip
- Access frontend via NodePort: http://<minikube-ip>:30000
- Or use: minikube service frontend-service -n todo-app
- Test sign up/sign in functionality
- Test chat interface
- Test task management via natural language
- Verify backend and MCP communication
- Reference: speckit.plan §Access Application

T-324: Use AI DevOps Tools
- Use Gordon for Docker operations (if available): "docker ai 'optimize my Dockerfile'"
- Use kubectl-ai: "kubectl-ai 'show pods in todo-app namespace'"
- Use kagent: "kagent 'check cluster health'"
- Document all AI commands used
- Reference: speckit.plan §AI DevOps Commands

T-325: Troubleshooting and Optimization
- Check logs if any pod fails: kubectl logs <pod-name> -n todo-app
- Describe pods for events: kubectl describe pod <pod-name> -n todo-app
- Verify resource usage: kubectl top pods -n todo-app
- Fix any issues and redeploy
- Reference: speckit.plan §Troubleshooting Guide

T-326: Documentation
- Update phase-4/README.md with:
  - Prerequisites (Docker, Minikube, kubectl, Helm)
  - Build instructions
  - Deployment instructions
  - How to access application
  - Troubleshooting guide
  - AI DevOps commands used
- Update CLAUDE.md with implementation notes
- Reference: speckit.specify §Acceptance Criteria

T-327: Create Demo and Verification
- Create demo video showing:
  - Minikube deployment process
  - Application running on K8s
  - Chat functionality working
  - kubectl commands showing pods/services
- Verify all acceptance criteria met
- Reference: speckit.specify §Acceptance Criteria

## Response snapshot

Generated comprehensive task list for Kubernetes Minikube deployment, organizing tasks by user stories with proper dependencies and parallel execution opportunities.

## Outcome

- ✅ Impact: Created complete task breakdown for Kubernetes deployment with 68 specific tasks organized by priority and user stories
- 🧪 Tests: none
- 📁 Files: specs/001-k8s-minikube-deployment/tasks.md
- 🔁 Next prompts: /sp.implement to execute the tasks
- 🧠 Reflection: Task organization enables independent implementation of user stories with clear MVP path starting from P1 story

## Evaluation notes (flywheel)

- Failure modes observed: None - successful generation of complete task breakdown
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute tasks with /sp.implement
