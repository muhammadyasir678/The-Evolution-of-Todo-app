# Phase 5: Advanced Cloud Deployment

This directory contains all files related to the Advanced Cloud Deployment of the Todo application with AI chatbot functionality. This phase introduces advanced features including recurring tasks, due date reminders, priority management, tagging system, and event-driven architecture using Kafka and Dapr.

## Overview

This phase focuses on implementing advanced cloud deployment features with:
- Recurring tasks with daily, weekly, monthly patterns
- Due date reminders with browser/email notifications
- Priority management (high, medium, low)
- Tagging system for tasks
- Advanced filtering and sorting
- Event-driven architecture using Kafka
- Dapr for standardized microservices patterns
- Real-time synchronization across devices
- Cloud deployment with auto-scaling and monitoring

## Architecture

### Event-Driven Architecture
- Kafka topics: `task-events`, `reminders`, `task-updates`
- Microservices for different concerns:
  - Recurring Task Service
  - Notification Service
  - Audit Service
  - WebSocket Service

### Dapr Integration
- Pub/Sub for Kafka messaging
- State management for conversation state
- Service invocation for inter-service communication
- Secrets management for credentials
- Jobs API for scheduled reminders

### Frontend Components
- TaskPriority: Priority selection component
- TaskTags: Tag management component
- TaskDueDate: Due date and reminder component
- TaskRecurrence: Recurrence pattern component
- TaskFilters: Multi-filter UI component
- TaskSearch: Instant search component

## Deployment

### Local Deployment (Minikube)
1. Deploy Kafka using Strimzi operator
2. Deploy Dapr to Minikube
3. Build Docker images for all services
4. Deploy using Helm chart

### Cloud Deployment (AKS/GKE/DOKS)
1. Set up cloud Kubernetes cluster
2. Configure managed Kafka (Redpanda Cloud or Confluent Cloud)
3. Install Dapr on cloud K8s
4. Deploy via CI/CD pipeline

## Directory Structure

```
phase-5/
├── services/
│   ├── recurring-task-service/
│   ├── notification-service/
│   ├── audit-service/
│   └── websocket-service/
├── frontend/
│   └── components/
├── backend/
├── k8s/
│   ├── kafka/
│   ├── dapr/
│   └── services/
├── helm-charts/
│   └── todo-app-v5/
├── scripts/
└── .github/
    └── workflows/
```

## Prerequisites

- Docker and Docker Compose
- kubectl
- Helm 3.x
- Dapr CLI
- Kafka client tools (for local development)
- Cloud provider account (for cloud deployment)

## Setup Instructions

### Local Development
1. Start Minikube with sufficient resources
2. Install Dapr in Minikube
3. Deploy Kafka using Strimzi
4. Build and deploy all services using Helm

### Cloud Deployment
1. Set up cloud Kubernetes cluster
2. Configure managed Kafka
3. Install Dapr on cloud cluster
4. Configure CI/CD pipeline with appropriate secrets
5. Push to main branch to trigger deployment

## Key Features

### Recurring Tasks
- Support for daily, weekly, monthly recurrence patterns
- Automatic creation of next occurrence when completed
- Configurable intervals (every X days/weeks/months)

### Due Date Reminders
- Configurable due dates with time
- Reminder scheduling before due date
- Browser push notifications and email delivery
- Integration with notification service

### Task Organization
- Priority levels (high, medium, low) with visual indicators
- Tagging system with autocomplete and management UI
- Multi-filter UI for priority, tags, status, due date range
- Sort by multiple fields with persistence

### Real-Time Sync
- WebSocket connections for real-time updates
- Task updates broadcast to all connected clients
- Cross-device synchronization

### Event-Driven Architecture
- All task operations publish events to Kafka
- Consumer services process events asynchronously
- Audit logging of all operations
- Decoupled service communication

## Monitoring and Logging

- Application logs aggregated via cloud provider
- Metrics collection using Prometheus/Grafana or cloud-native equivalents
- Health monitoring with alerts for failures
- Audit trails for compliance

## Security

- Dapr secrets management for credential handling
- TLS encryption for all service communications
- Role-based access control for task operations
- Secure handling of sensitive data in Kubernetes Secrets

## Dependency Management

This project uses `uv` for fast dependency management. See [DEPENDENCIES_WITH_UV.md](./DEPENDENCIES_WITH_UV.md) for detailed instructions on managing dependencies with `uv`.

To install dependencies for all services:
```bash
bash scripts/install-dependencies-with-uv.sh
```