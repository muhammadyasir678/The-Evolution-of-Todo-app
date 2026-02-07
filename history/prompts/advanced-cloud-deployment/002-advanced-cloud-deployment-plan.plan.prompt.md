---
id: 2
title: advanced-cloud-deployment-plan
stage: plan
date_iso: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: advanced-cloud-deployment
branch: 002-advanced-cloud-deployment
user: user
command: /sp.plan
labels:
  - planning
  - architecture
  - kafka
  - dapr
  - microservices
links:
  spec: ./spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/002-advanced-cloud-deployment/plan.md
  - specs/002-advanced-cloud-deployment/research.md
  - specs/002-advanced-cloud-deployment/data-model.md
  - specs/002-advanced-cloud-deployment/quickstart.md
  - specs/002-advanced-cloud-deployment/contracts/task-api.yaml
  - specs/002-advanced-cloud-deployment/contracts/websocket-api.yaml
tests_yaml: []
outcome: Created comprehensive implementation plan for advanced cloud deployment featuring recurring tasks, due date reminders, event-driven architecture with Kafka and Dapr
evaluation: Plan includes technical context, research, data models, quickstart guide, and API contracts for all required microservices
---

## Prompt
```
PHASE: Phase V - Advanced Cloud Deployment

BASE: Approved speckit.specify for Phase V

ARCHITECTURE:

Project Structure:
phase-5/
├── services/
│   ├── recurring-task-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   ├── notification-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   ├── audit-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   └── websocket-service/
│       ├── src/
│       ├── Dockerfile
│       └── pyproject.toml
├── frontend/              (extends Phase III frontend)
│   ├── components/
│   │   ├── TaskFilters.tsx
│   │   ├── TaskPriority.tsx
│   │   ├── TaskTags.tsx
│   │   ├── TaskRecurrence.tsx
│   │   └── TaskDueDate.tsx
├── backend/               (extends Phase III backend)
│   ├── app/
│   │   ├── routes/
│   │   │   └── tasks.py (extend with new fields)
│   │   ├── models.py (extend Task model)
│   │   └── kafka_producer.py
├── k8s/
│   ├── kafka/
│   │   └── strimzi-kafka.yaml
│   ├── dapr/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   ├── secretstore.yaml
│   │   └── bindings.yaml
│   └── services/
│       ├── recurring-task-deployment.yaml
│       ├── notification-deployment.yaml
│       ├── audit-deployment.yaml
│       └── websocket-deployment.yaml
├── helm-charts/
│   └── todo-app-v5/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── scripts/
│   ├── deploy-minikube-v5.sh
│   └── deploy-cloud.sh
└── README.md
DATA MODEL EXTENSIONS:

Task (extended from Phase III):
- id: integer (existing)
- user_id: string (existing)
- title: string (existing)
- description: text (existing)
- completed: boolean (existing)
- created_at: timestamp (existing)
- updated_at: timestamp (existing)
- priority: enum ("high", "medium", "low") - NEW
- tags: array of strings - NEW
- due_date: timestamp (nullable) - NEW
- reminder_time: timestamp (nullable) - NEW
- recurrence_pattern: string (nullable: "daily", "weekly", "monthly") - NEW
- recurrence_interval: integer (nullable: e.g., every 2 weeks) - NEW
- parent_task_id: integer (nullable, for recurring tasks) - NEW

AuditLog:
- id: integer
- user_id: string
- task_id: integer
- action: string ("created", "updated", "deleted", "completed")
- details: jsonb
- timestamp: timestamp

EVENT SCHEMAS:

TaskEvent (task-events topic):
```json
{
  "event_type": "created" | "updated" | "completed" | "deleted",
  "task_id": 123,
  "user_id": "user_abc",
  "task_data": { /* full task object */ },
  "timestamp": "2026-01-18T10:30:00Z"
}
```

ReminderEvent (reminders topic):
```json
{
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Submit report",
  "due_at": "2026-01-19T17:00:00Z",
  "remind_at": "2026-01-19T16:00:00Z",
  "timestamp": "2026-01-18T10:30:00Z"
}
```

TaskUpdateEvent (task-updates topic):
```json
{
  "user_id": "user_abc",
  "task_id": 123,
  "action": "created",
  "task_data": { /* full task object */ },
  "timestamp": "2026-01-18T10:30:00Z"
}
```

KAFKA ARCHITECTURE:

Topics:
- task-events (partitions: 3, retention: 7 days)
- reminders (partitions: 1, retention: 1 day)
- task-updates (partitions: 3, retention: 1 hour)

Producers:
- Backend API: Publishes to all three topics on task operations

Consumers:
- Recurring Task Service: Consumes task-events (completed events)
- Notification Service: Consumes reminders
- Audit Service: Consumes task-events
- WebSocket Service: Consumes task-updates

DAPR COMPONENTS:

1. Pub/Sub Component (pubsub.yaml):
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
    value: "kafka-broker:9092"  # or Redpanda Cloud URL
  - name: authType
    value: "password"
  - name: saslUsername
    secretKeyRef:
      name: kafka-secrets
      key: username
  - name: saslPassword
    secretKeyRef:
      name: kafka-secrets
      key: password
```

2. State Store Component (statestore.yaml):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: db-secrets
      key: connectionString
```

3. Secret Store Component (secretstore.yaml):
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
```

4. Jobs API for Reminders (via Dapr Jobs API):
- Schedule reminder at exact due_date - reminder_time
- Callback endpoint triggers notification

MICROSERVICES DESIGN:

1. Recurring Task Service:
- Subscribes to task-events topic
- Filters for: event_type == "completed" AND recurrence_pattern != null
- Logic:
  - Calculate next occurrence date
  - Create new task with same title, description, priority, tags
  - Set parent_task_id to original task
  - Publish task-events "created"

2. Notification Service:
- Subscribes to reminders topic
- Sends notifications via:
  - Browser push notifications (Web Push API)
  - Email (SendGrid/AWS SES)
- Logs notification delivery status

3. Audit Service:
- Subscribes to task-events topic
- Inserts all events into audit_log table
- Provides audit trail for compliance

4. WebSocket Service:
- Subscribes to task-updates topic
- Maintains WebSocket connections per user
- Broadcasts task changes to all user's connected clients
- Enables real-time sync across devices

BACKEND CHANGES:

Kafka Producer Integration:
```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BROKERS"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# After creating task
producer.send("task-events", {
    "event_type": "created",
    "task_id": task.id,
    "user_id": user_id,
    "task_data": task.dict(),
    "timestamp": datetime.utcnow().isoformat()
})

# If task has due_date and reminder_time
if task.due_date and task.reminder_time:
    producer.send("reminders", {
        "task_id": task.id,
        "user_id": user_id,
        "title": task.title,
        "due_at": task.due_date.isoformat(),
        "remind_at": task.reminder_time.isoformat(),
        "timestamp": datetime.utcnow().isoformat()
    })

# For real-time sync
producer.send("task-updates", {
    "user_id": user_id,
    "task_id": task.id,
    "action": "created",
    "task_data": task.dict(),
    "timestamp": datetime.utcnow().isoformat()
})
```

Extended API Endpoints:
- GET /api/{user_id}/tasks?priority=high&tags=work&due_before=2026-01-20
- GET /api/{user_id}/tasks/search?q=meeting
- POST /api/{user_id}/tasks (accepts new fields)
- GET /api/{user_id}/tags (list all user's tags)

FRONTEND CHANGES:

New Components:
- TaskPriority: Dropdown for High/Medium/Low
- TaskTags: Tag selector with autocomplete
- TaskDueDate: Date/time picker
- TaskRecurrence: Recurrence pattern selector
- TaskFilters: Multi-filter UI
- TaskSearch: Search bar with instant results

WebSocket Integration:
```typescript
const ws = new WebSocket(`ws://backend-service:8000/ws/${userId}`)
ws.onmessage = (event) => {
  const taskUpdate = JSON.parse(event.data)
  // Update UI optimistically
  updateTaskInList(taskUpdate.task_data)
}
```

DAPR USAGE PATTERNS:

Publishing Events (Backend):
```python
import httpx

# Publish via Dapr Pub/Sub
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
    json=event_data
)
```

Consuming Events (Services):
```python
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub_name="kafka-pubsub", topic="task-events")
async def handle_task_event(event: dict):
    if event["event_type"] == "completed" and event["task_data"].get("recurrence_pattern"):
        # Create next occurrence
        pass
```

Scheduling Reminders (Dapr Jobs API):
```python
await httpx.post(
    f"http://localhost:3500/v1.0-alpha1/jobs/reminder-{task_id}",
    json={
        "dueTime": remind_at.isoformat(),
        "data": {
            "task_id": task_id,
            "user_id": user_id,
            "type": "reminder"
        }
    }
)
```

KUBERNETES DEPLOYMENT (LOCAL - MINIKUBE):

Install Kafka (Strimzi):
```bash
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka
kubectl apply -f k8s/kafka/strimzi-kafka.yaml
```

Install Dapr:
```bash
dapr init -k
kubectl apply -f k8s/dapr/
```

Deploy Services:
```bash
helm install todo-app-v5 helm-charts/todo-app-v5 -n todo-app
```

KUBERNETES DEPLOYMENT (CLOUD):

Cloud Provider Setup:
- Azure: Create AKS cluster, configure kubectl
- Google Cloud: Create GKE cluster, configure kubectl
- DigitalOcean: Create DOKS cluster, configure kubectl

Managed Kafka:
- Redpanda Cloud: Create serverless cluster, get bootstrap URL and credentials
- Confluent Cloud: Create cluster, create topics, get credentials

Update Dapr pubsub.yaml with cloud Kafka credentials

Install Dapr on Cloud K8s:
```bash
dapr init -k
```

Deploy via CI/CD (GitHub Actions)

CI/CD PIPELINE:

GitHub Actions Workflow (.github/workflows/deploy.yml):
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

      - name: Build and Push Images
        run: |
          docker build -t ghcr.io/${{ github.repository }}/frontend:${{ github.sha }} frontend/
          docker push ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
          # Repeat for backend, mcp-server, new services

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install todo-app-v5 helm-charts/todo-app-v5 \
            --set frontend.image.tag=${{ github.sha }} \
            --set backend.image.tag=${{ github.sha }} \
            -n todo-app
```

MONITORING & LOGGING:

Logging:
- Aggregate logs from all services
- Use cloud provider logging (Azure Monitor, GCP Cloud Logging, DO Monitoring)
- Or deploy ELK/Loki stack

Metrics:
- Prometheus for metrics collection
- Grafana for visualization
- Or use cloud provider metrics

Alerts:
- Pod crash alerts
- High error rate alerts
- Resource exhaustion alerts

TESTING STRATEGY:

Unit Tests:
- Test each new service independently
- Test event publishing and consuming
- Test Dapr integration

Integration Tests:
- Test end-to-end event flows
- Test recurring task creation
- Test reminder scheduling and triggering
- Test real-time sync

Load Tests:
- Simulate multiple users
- Test Kafka throughput
- Test auto-scaling

EXIT CRITERIA:
- All advanced features implemented and functional
- Kafka topics created and operational
- All 4 new services deployed and consuming events
- Dapr installed and all building blocks functional
- Recurring tasks auto-created on completion
- Reminders scheduled and triggered accurately
- Real-time sync working across clients
- Audit log capturing all operations
- Deployed locally to Minikube successfully
- Deployed to cloud K8s (AKS/GKE/DOKS) successfully
- Managed Kafka integrated (Redpanda Cloud or Confluent)
- CI/CD pipeline operational
- Monitoring and logging configured
- All tests passing
- Documentation complete
```

## Response
Created comprehensive implementation plan for advanced cloud deployment featuring recurring tasks, due date reminders, priority management, tagging system, and event-driven architecture using Kafka and Dapr. The plan includes:

1. Implementation Plan (plan.md) - Complete architecture and technical context
2. Research Document (research.md) - Technology decisions and best practices
3. Data Model (data-model.md) - Extended task entity and event schemas
4. Quickstart Guide (quickstart.md) - Setup and deployment instructions
5. API Contracts (contracts/) - OpenAPI specifications for task and WebSocket APIs

The plan covers the four dedicated microservices (Recurring Task, Notification, Audit, WebSocket), extended frontend components, backend modifications, Kafka integration, Dapr setup, and deployment strategies for both local (Minikube) and cloud (AKS/GKE/DOKS) environments.