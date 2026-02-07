---
id: 0002
title: k8s-minikube-deployment-plan
stage: plan
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-k8s-minikube-deployment
branch: 001-k8s-minikube-deployment
user: unknown
command: /sp.plan
labels: ["kubernetes", "docker", "helm", "minikube", "deployment", "containerization", "planning"]
links:
  spec: ../specs/001-k8s-minikube-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-k8s-minikube-deployment/plan.md
  - specs/001-k8s-minikube-deployment/research.md
  - specs/001-k8s-minikube-deployment/data-model.md
  - specs/001-k8s-minikube-deployment/quickstart.md
  - specs/001-k8s-minikube-deployment/contracts/backend-api.yaml
tests:
  - none
---

## Prompt

PHASE: Phase IV - Local Kubernetes Deployment (Minikube)

BASE: Approved speckit.specify for Phase IV

ARCHITECTURE:

Project Structure:
phase-4/
├── docker/
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   ├── mcp-server.Dockerfile
│   └── docker-compose.yml
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── mcp-deployment.yaml
│   └── mcp-service.yaml
├── helm-charts/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── namespace.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── mcp-deployment.yaml
│           └── mcp-service.yaml
├── scripts/
│   ├── build-images.sh
│   ├── push-images.sh
│   └── deploy-minikube.sh
├── README.md
└── CLAUDE.md

DOCKER STRATEGY:

Frontend Dockerfile (Multi-stage):
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
RUN npm ci --production
EXPOSE 3000
CMD ["npm", "start"]
```

Backend Dockerfile (Multi-stage):
```dockerfile
# Stage 1: Build
FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system -r pyproject.toml

# Stage 2: Production
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

MCP Server Dockerfile:
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system -r pyproject.toml
COPY . .
CMD ["python", "src/server.py"]
```

docker-compose.yml:
```yaml
services:
  frontend:
    build:
      context: ../phase-3/frontend
      dockerfile: ../../phase-4/docker/frontend.Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build:
      context: ../phase-3/backend
      dockerfile: ../../phase-4/docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    depends_on:
      - mcp-server

  mcp-server:
    build:
      context: ../phase-3/mcp-server
      dockerfile: ../../phase-4/docker/mcp-server.Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
```

KUBERNETES ARCHITECTURE:

Namespace:
- Create dedicated namespace: todo-app

ConfigMap (non-sensitive config):
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
data:
  NEXT_PUBLIC_API_URL: "http://backend-service:8000"
  BACKEND_PORT: "8000"
  FRONTEND_PORT: "3000"
```

Secret (sensitive data):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded>
  OPENAI_API_KEY: <base64-encoded>
  BETTER_AUTH_SECRET: <base64-encoded>
```

Frontend Deployment:
- Image: todo-frontend:latest
- Replicas: 2
- Port: 3000
- Environment: ConfigMap + Secrets
- Resources: requests (100m CPU, 128Mi memory), limits (200m CPU, 256Mi memory)
- Readiness probe: HTTP GET /
- Liveness probe: HTTP GET /

Backend Deployment:
- Image: todo-backend:latest
- Replicas: 2
- Port: 8000
- Environment: ConfigMap + Secrets
- Resources: requests (200m CPU, 256Mi memory), limits (500m CPU, 512Mi memory)
- Readiness probe: HTTP GET /health
- Liveness probe: HTTP GET /health

MCP Server Deployment:
- Image: todo-mcp-server:latest
- Replicas: 1
- Environment: Secrets (DATABASE_URL)
- Resources: requests (100m CPU, 128Mi memory), limits (200m CPU, 256Mi memory)

Services:
- frontend-service: NodePort (30000) for external access
- backend-service: ClusterIP (internal only)
- mcp-service: ClusterIP (internal only)

HELM CHART STRUCTURE:

Chart.yaml:
```yaml
apiVersion: v2
name: todo-app
description: AI-powered Todo application
version: 1.0.0
appVersion: "1.0"
```

values.yaml:
```yaml
frontend:
  image: todo-frontend
  tag: latest
  replicas: 2
  port: 3000
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi

backend:
  image: todo-backend
  tag: latest
  replicas: 2
  port: 8000
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

mcpServer:
  image: todo-mcp-server
  tag: latest
  replicas: 1

secrets:
  databaseUrl: ""
  openaiApiKey: ""
  betterAuthSecret: ""
```

Templates:
- Use {{ .Values.frontend.replicas }} for parameterization
- Support environment-specific overrides
- Include all K8s manifests as templates

MINIKUBE DEPLOYMENT FLOW:

Setup:
1. Install Minikube: `minikube start`
2. Enable addons: `minikube addons enable ingress`
3. Set Docker environment: `eval $(minikube docker-env)`

Build Images:
1. Build in Minikube Docker: `docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../phase-3/frontend`
2. Build backend and MCP server similarly
3. Verify images: `docker images | grep todo`

Deploy with Helm:
1. Create namespace: `kubectl create namespace todo-app`
2. Create secrets: `kubectl create secret generic todo-secrets --from-literal=DATABASE_URL=... -n todo-app`
3. Install chart: `helm install todo-app helm-charts/todo-app -n todo-app`
4. Verify: `kubectl get pods -n todo-app`

Access Application:
1. Get Minikube IP: `minikube ip`
2. Access frontend: `http://<minikube-ip>:30000`
3. Or use tunnel: `minikube service frontend-service -n todo-app`

AI DEVOPS COMMANDS:

Docker AI (Gordon) - if available:
```bash
docker ai "Create optimized Dockerfile for Next.js production"
docker ai "Build multi-stage Dockerfile for FastAPI Python app"
docker ai "Show me how to reduce image size"
```

kubectl-ai:
```bash
kubectl-ai "deploy todo frontend with 2 replicas"
kubectl-ai "scale backend to 3 replicas"
kubectl-ai "show me all pods in todo-app namespace"
kubectl-ai "check why pods are failing"
```

kagent:
```bash
kagent "analyze cluster health"
kagent "why is my backend pod crashing?"
kagent "optimize resource allocation for todo-app"
```

TROUBLESHOOTING GUIDE:

Common Issues:
1. ImagePullBackOff: Images not in Minikube Docker
   - Solution: Build with `eval $(minikube docker-env)`
2. CrashLoopBackOff: Missing environment variables
   - Solution: Check secrets are created
3. Service not accessible: NodePort not working
   - Solution: Use `minikube service` command
4. Database connection fails: Neon not accessible
   - Solution: Check DATABASE_URL and network connectivity

Health Checks:
```bash
kubectl get pods -n todo-app
kubectl logs <pod-name> -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

TESTING STRATEGY:

Docker Testing:
- Run docker-compose up locally
- Verify all services start
- Test frontend → backend → MCP → database flow

Kubernetes Testing:
- Deploy to Minikube
- Verify all pods Running
- Test service connectivity (exec into pod, curl services)
- Test frontend accessibility via NodePort
- Test full chat functionality end-to-end

EXIT CRITERIA:
- All Dockerfiles created with multi-stage builds
- docker-compose.yml working locally
- All K8s manifests created and valid
- Helm chart packages entire application
- Application deployed to Minikube successfully
- All pods in Running state
- Frontend accessible via browser
- Backend and MCP server communicating
- Chat functionality working on K8s
- AI DevOps tools used and documented
- README with complete setup instructions

## Response snapshot

Completed comprehensive implementation plan for Kubernetes Minikube deployment, including technical context, constitution check, project structure, research findings, data model, quickstart guide, and API contracts.

## Outcome

- ✅ Impact: Created complete planning artifacts for Kubernetes containerization and deployment including Dockerfiles, K8s manifests, Helm chart structure, and deployment guides
- 🧪 Tests: none
- 📁 Files: specs/001-k8s-minikube-deployment/plan.md, specs/001-k8s-minikube-deployment/research.md, specs/001-k8s-minikube-deployment/data-model.md, specs/001-k8s-minikube-deployment/quickstart.md, specs/001-k8s-minikube-deployment/contracts/backend-api.yaml
- 🔁 Next prompts: /sp.tasks to generate implementation tasks, /sp.implement to execute the tasks
- 🧠 Reflection: Planning phase established clear technical approach with proper separation of concerns across containerization, orchestration, and packaging layers with comprehensive documentation for successful Kubernetes deployment

## Evaluation notes (flywheel)

- Failure modes observed: None - successful creation of complete planning artifacts
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation for implementation
