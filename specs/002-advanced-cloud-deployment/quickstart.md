# Quickstart Guide: Advanced Cloud Deployment

**Feature**: Advanced Cloud Deployment (Phase V)
**Date**: 2026-02-05
**Branch**: 002-advanced-cloud-deployment

## Overview

This quickstart guide provides instructions for setting up, running, and deploying the Advanced Cloud Deployment feature with recurring tasks, due date reminders, event-driven architecture, and cloud deployment capabilities.

## Prerequisites

### Local Development
- Docker and Docker Compose (v20+)
- Minikube (v1.28+)
- kubectl (v1.25+)
- Dapr CLI (v1.11+)
- Python 3.11+
- Node.js 18+ / npm 9+
- Java 11+ (for Kafka management tools)

### Cloud Deployment
- Access to Azure, Google Cloud, or DigitalOcean account
- kubectl configured for cloud cluster
- Dapr installed on cloud cluster
- Managed Kafka service (Redpanda Cloud or Confluent Cloud)
- Container registry access (GHCR, Docker Hub, or cloud provider)

## Local Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd The-Evolution-of-Todo-app
git checkout 002-advanced-cloud-deployment
```

### 2. Install Dapr Locally
```bash
dapr init
dapr uninstall  # if previously installed
dapr init -k    # initialize Dapr in Kubernetes mode
```

### 3. Start Minikube
```bash
minikube start --cpus=4 --memory=8192 --disk-size=40g
minikube addons enable ingress
```

### 4. Deploy Kafka to Minikube
```bash
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
kubectl apply -f k8s/kafka/strimzi-kafka.yaml
kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka
```

### 5. Apply Dapr Components
```bash
kubectl apply -f k8s/dapr/pubsub.yaml
kubectl apply -f k8s/dapr/statestore.yaml
kubectl apply -f k8s/dapr/secretstore.yaml
kubectl apply -f k8s/dapr/bindings.yaml
```

### 6. Build and Deploy Services
```bash
# Build Docker images
docker build -t todo-frontend:latest -f frontend/Dockerfile .
docker build -t todo-backend:latest -f backend/Dockerfile .
docker build -t recurring-task-service:latest -f services/recurring-task-service/Dockerfile .
docker build -t notification-service:latest -f services/notification-service/Dockerfile .
docker build -t audit-service:latest -f services/audit-service/Dockerfile .
docker build -t websocket-service:latest -f services/websocket-service/Dockerfile .

# Deploy using Helm
helm install todo-app-v5 helm-charts/todo-app-v5 -n todo-app --create-namespace
```

## Running the System

### 1. Verify Deployments
```bash
kubectl get pods -n todo-app
kubectl get svc -n todo-app
kubectl logs -f deployment/recurring-task-service -n todo-app
```

### 2. Check Dapr Status
```bash
dapr status -k
dapr list -k
```

### 3. Access the Application
```bash
# Get the frontend service IP
minikube service frontend-service -n todo-app --url

# Or set up port forwarding
kubectl port-forward svc/frontend-service 3000:80 -n todo-app
```

## Configuration

### Environment Variables

#### Backend Service
```bash
export DATABASE_URL="postgresql://username:password@neon-host.region.provider.neon.tech/dbname"
export KAFKA_BROKERS="kafka.kafka.svc.cluster.local:9092"
export DAPR_HTTP_ENDPOINT="http://localhost:3500"
export DAPR_GRPC_ENDPOINT="http://localhost:50001"
```

#### Microservices
Each service needs:
- KAFKA_BROKERS: Kafka broker addresses
- DAPR_HTTP_ENDPOINT: Dapr sidecar endpoint
- DATABASE_URL: PostgreSQL connection string
- SERVICE_PORT: Internal service port

### Dapr Components Configuration

#### Kafka Pub/Sub Component
Located at `k8s/dapr/pubsub.yaml`:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka.kafka.svc.cluster.local:9092"  # Update for cloud
  - name: authType
    value: "plaintext"  # Change to "mtls" or "saslPlaintext" for production
```

## Key Features Walkthrough

### 1. Creating Recurring Tasks
```bash
# Create a recurring task via API
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly team meeting",
    "recurrence_pattern": "weekly",
    "recurrence_interval": 1
  }'
```

### 2. Setting Up Due Date Reminders
```bash
# Create a task with due date and reminder
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Submit report",
    "due_date": "2026-01-19T17:00:00Z",
    "reminder_time": 3600
  }'
```

### 3. Using Priority and Tags
```bash
# Create task with priority and tags
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Critical bug fix",
    "priority": "high",
    "tags": ["bug", "urgent", "backend"],
    "due_date": "2026-01-20T10:00:00Z"
  }'
```

### 4. Filtering and Searching
```bash
# Filter tasks by priority and tags
curl "http://localhost:8000/api/user123/tasks?priority=high,tags=urgent&due_before=2026-01-25"

# Search tasks
curl "http://localhost:8000/api/user123/tasks/search?q=report"
```

## Cloud Deployment

### 1. Prepare Cloud Environment
```bash
# For Azure AKS
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# For Google GKE
gcloud container clusters get-credentials my-cluster --zone us-central1-a --project my-project

# For DigitalOcean DOKS
doctl kubernetes cluster kubeconfig save my-cluster
```

### 2. Set Up Managed Kafka
Choose one:
- Redpanda Cloud: Create cluster and get connection details
- Confluent Cloud: Create cluster and topics, get credentials

### 3. Update Dapr Configuration
Modify `k8s/dapr/pubsub.yaml` with cloud Kafka credentials:
```yaml
- name: brokers
  value: "pkc-XXXXX.region.provider.confluent.cloud:9092"  # Confluent
  # OR
  # value: "pkc-XXXXX.region.redpanda.cloud:9092"  # Redpanda
- name: saslUsername
  value: "{{.confluent-api-key}}"
- name: saslPassword
  value: "{{.confluent-api-secret}}"
```

### 4. Deploy to Cloud
```bash
# Build and push images to container registry
docker build -t ghcr.io/username/repo/frontend:latest ./frontend
docker push ghcr.io/username/repo/frontend:latest

# Deploy using Helm with cloud-specific values
helm upgrade --install todo-app-v5 ./helm-charts/todo-app-v5 \
  --values ./helm-charts/todo-app-v5/values-cloud.yaml \
  --set frontend.image.tag=latest \
  --set backend.image.tag=latest \
  -n todo-app --create-namespace
```

## CI/CD Pipeline

### GitHub Actions Workflow
The CI/CD pipeline is defined in `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      # Build, push, and deploy steps...
```

### Required GitHub Secrets
- `KUBE_CONFIG`: Kubernetes configuration file content
- `CONFLUENT_API_KEY`: Managed Kafka API key
- `CONFLUENT_API_SECRET`: Managed Kafka API secret

## Monitoring and Logging

### Local Monitoring
```bash
# Port forward to Prometheus
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring

# Port forward to Grafana
kubectl port-forward svc/grafana 3001:80 -n monitoring
```

### Key Metrics to Monitor
- Kafka topic lag for each consumer group
- Service response times and error rates
- Database connection pool utilization
- Dapr sidecar health and performance

## Troubleshooting

### Common Issues

#### Kafka Connection Problems
```bash
# Check Kafka pods
kubectl get pods -n kafka
kubectl logs -f deployment/my-cluster-kafka -n kafka

# Verify Kafka endpoints
kubectl get svc -n kafka
```

#### Dapr Sidecar Issues
```bash
# Check Dapr status
dapr status -k
kubectl get pods -l app.kubernetes.io/part-of=dapr

# Check Dapr logs
kubectl logs -f deployment/dapr-placement-server -n dapr-system
```

#### Service Discovery Issues
```bash
# Check service endpoints
kubectl get endpoints -n todo-app
kubectl describe svc backend-service -n todo-app
```

### Useful Commands
```bash
# Check all system status
kubectl get all -n todo-app

# View application logs
kubectl logs -f deployment/backend -n todo-app

# Execute commands in pods
kubectl exec -it deployment/backend -n todo-app -- /bin/sh

# Debug Kafka topics
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Development Workflow

### Adding New Services
1. Create service directory with Dockerfile and pyproject.toml
2. Implement Dapr pub/sub subscriber pattern
3. Add Kubernetes deployment manifest
4. Update Helm chart
5. Update documentation

### Testing Event Flows
1. Use Kafka console tools to inspect messages:
```bash
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic task-events --from-beginning
```

2. Test end-to-end scenarios with Postman/Newman or custom scripts
3. Verify event ordering and processing correctness

## Performance Tuning

### Kafka Optimization
- Adjust partition count based on throughput requirements
- Tune replication factor for durability vs. performance
- Configure appropriate retention policies

### Service Scaling
- Use Horizontal Pod Autoscaler (HPA) for dynamic scaling
- Configure resource limits and requests appropriately
- Implement circuit breakers for resilience

### Database Optimization
- Ensure proper indexing based on query patterns
- Optimize connection pooling settings
- Use read replicas for read-heavy operations