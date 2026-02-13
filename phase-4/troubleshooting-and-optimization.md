# Troubleshooting and Optimization Guide: Advanced Cloud Deployment

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Kafka Connection Problems
**Symptoms**: Services can't publish/consume events, error messages about Kafka connection failures
**Diagnosis**:
```bash
# Check Kafka pods status
kubectl get pods -n kafka

# Check Kafka logs
kubectl logs -f deployment/my-cluster-kafka -n kafka

# Verify Kafka service is accessible
kubectl get svc -n kafka

# Test Kafka connectivity from inside cluster
kubectl run kafka-test -it --rm --image=busybox:1.28 --restart=Never -- sh
# Inside the pod:
# nc my-cluster-kafka-brokers.kafka.svc.cluster.local 9092
```

**Solutions**:
1. Verify Kafka cluster is running: `kubectl get kafka -n kafka`
2. Check Strimzi operator logs: `kubectl logs -f deployment/strimzi-cluster-operator -n kafka`
3. Ensure Kafka service is accessible from other namespaces
4. Verify network policies allow communication between namespaces

#### 2. Dapr Sidecar Issues
**Symptoms**: Services can't communicate via Dapr, error messages about Dapr sidecar not found
**Diagnosis**:
```bash
# Check Dapr status
dapr status -k

# List Dapr applications
dapr list -k

# Check Dapr system pods
kubectl get pods -n dapr-system

# Check Dapr sidecar logs for a specific pod
kubectl logs -c daprd <pod-name> -n <namespace>
```

**Solutions**:
1. Verify Dapr is installed: `kubectl get pods -n dapr-system`
2. Check Dapr components: `kubectl get components.dapr.io -A`
3. Verify Dapr annotations in deployment manifests
4. Restart problematic pods: `kubectl delete pod <pod-name> -n <namespace>`

#### 3. Recurring Task Service Not Processing Events
**Symptoms**: Completed recurring tasks don't generate next occurrence
**Diagnosis**:
```bash
# Check Recurring Task Service logs
kubectl logs -f deployment/recurring-task-service -n todo-app

# Verify events are published to Kafka
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic task-events --from-beginning

# Check if service is subscribed to correct topic
kubectl describe deployment/recurring-task-service -n todo-app
```

**Solutions**:
1. Verify Dapr subscription annotation in deployment
2. Check Kafka topic exists: `kubectl exec -it my-cluster-kafka-0 -n kafka -- \
   bin/kafka-topics.sh --describe --topic task-events --bootstrap-server localhost:9092`
3. Confirm recurrence pattern is valid in task data
4. Verify service has proper permissions to create new tasks

#### 4. Notification Service Not Sending Notifications
**Symptoms**: Due date reminders not delivered to users
**Diagnosis**:
```bash
# Check Notification Service logs
kubectl logs -f deployment/notification-service -n todo-app

# Verify reminder events are published
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic reminders --from-beginning

# Check notification service configuration
kubectl describe deployment/notification-service -n todo-app
```

**Solutions**:
1. Verify notification service is subscribed to reminders topic
2. Check if notification credentials are properly configured
3. Confirm notification preferences are set for users
4. Verify service has access to send notifications (email, push)

#### 5. WebSocket Service Not Broadcasting Updates
**Symptoms**: Task updates not appearing in real-time across devices
**Diagnosis**:
```bash
# Check WebSocket Service logs
kubectl logs -f deployment/websocket-service -n todo-app

# Verify WebSocket service is accessible
kubectl get svc websocket-service -n todo-app

# Test WebSocket connection
kubectl port-forward svc/websocket-service 8004:8004 -n todo-app
# Then test connection with a WebSocket client
```

**Solutions**:
1. Verify WebSocket service is subscribed to task-updates topic
2. Check if clients are connecting properly to WebSocket service
3. Confirm service can broadcast to multiple connections
4. Verify Dapr pub/sub configuration

#### 6. Database Connection Issues
**Symptoms**: Services can't connect to PostgreSQL database
**Diagnosis**:
```bash
# Check database connection from a pod
kubectl run pg-test -it --rm --image=postgres:13 --restart=Never -- psql -h <db-host> -U <db-user> -d <db-name>

# Check if database secrets are properly mounted
kubectl describe deployment/<service-name> -n todo-app

# Check service logs for database errors
kubectl logs deployment/backend -n todo-app
```

**Solutions**:
1. Verify database connection string in secrets
2. Check if Neon PostgreSQL is accessible from cluster
3. Confirm database credentials are correct
4. Verify network connectivity to external database

### Diagnostic Commands

#### Check Overall System Health
```bash
# Check all pods in todo-app namespace
kubectl get pods -n todo-app

# Check all services in todo-app namespace
kubectl get svc -n todo-app

# Check all deployments in todo-app namespace
kubectl get deployments -n todo-app

# Check Kafka topics and status
kubectl get kafka -n kafka
kubectl get kafkatopics -n kafka

# Check Dapr components
kubectl get components.dapr.io -A
kubectl get configurations.dapr.io -A
```

#### Monitor Resource Usage
```bash
# Check resource usage of pods
kubectl top pods -n todo-app

# Check resource usage of nodes
kubectl top nodes

# Describe specific pod for detailed info
kubectl describe pod <pod-name> -n todo-app
```

#### Check Logs Across Services
```bash
# Get logs from all pods in todo-app namespace
kubectl get pods -n todo-app -o jsonpath='{.items[*].metadata.name}' | xargs -I {} kubectl logs {} -n todo-app

# Follow logs from a specific service
kubectl logs -f deployment/backend -n todo-app

# Check logs for errors
kubectl logs deployment/backend -n todo-app | grep -i error
```

## Optimization Guide

### Resource Optimization

#### CPU and Memory Requests/Limits
Review and adjust resource requests and limits in deployment manifests:

```yaml
# Example optimized resource configuration
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### Horizontal Pod Autoscaling
Create HPA configurations for services that need auto-scaling:

```bash
# Create HPA for backend service
kubectl autoscale deployment backend --cpu-percent=70 --min=1 --max=10 -n todo-app

# Create HPA for frontend service
kubectl autoscale deployment frontend --cpu-percent=70 --min=1 --max=5 -n todo-app
```

### Kafka Optimization

#### Topic Configuration
Optimize Kafka topic settings for performance:

```yaml
# Example optimized Kafka topic configuration
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 6  # Increase partitions for higher throughput
  replicas: 3    # Ensure durability
  config:
    retention.ms: 86400000  # 24 hours retention
    segment.bytes: 1073741824  # 1 GiB segments
    min.insync.replicas: 2  # Ensure durability
```

#### Consumer Group Optimization
Optimize consumer group settings in service configurations:

```yaml
# Example consumer configuration
consumer:
  group.id: "optimized-consumer-group"
  max.poll.records: 100  # Process more records per poll
  max.poll.interval.ms: 300000  # 5 minute max processing time
  session.timeout.ms: 10000  # 10 second session timeout
  heartbeat.interval.ms: 3000  # 3 second heartbeat
```

### Database Optimization

#### Connection Pooling
Optimize database connection pooling in service configurations:

```python
# Example connection pool optimization in Python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # Initial connections
    max_overflow=30,  # Extra connections during high load
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,  # Recycle connections every hour
)
```

### Dapr Optimization

#### Component Configuration
Optimize Dapr component configurations:

```yaml
# Optimized pubsub component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-brokers.kafka.svc.cluster.local:9092"
  - name: authType
    value: "plaintext"
  - name: maxMessageBytes
    value: "1048576"  # 1MB max message size
  - name: consumerMaxWaitTime
    value: "100"  # 100ms max wait time
  - name: publishTimeout
    value: "30"  # 30s publish timeout
```

### Network Optimization

#### Service Mesh Configuration
Optimize service-to-service communication:

```yaml
# Example service configuration with optimized networking
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: todo-app
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: backend
  topologyKeys:  # Optimize for same-node communication first
    - "kubernetes.io/hostname"
    - "*"
```

### Monitoring and Observability

#### Health Checks
Ensure all services have proper health checks:

```yaml
# Example health check configuration
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

#### Metrics Collection
Enable metrics collection for performance monitoring:

```bash
# Check metrics for pods
kubectl top pods -n todo-app

# View metrics in Prometheus (if deployed)
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
```

### Performance Testing

#### Load Testing Script
Create a load testing script to validate optimizations:

```bash
# Example load testing with hey (HTTP load generator)
hey -n 1000 -c 10 -m POST -H "Content-Type: application/json" \
  -d '{"title":"Load test task", "description":"Created during load testing"}' \
  http://<frontend-service-ip>/api/test-user/tasks
```

#### Resource Monitoring During Load
Monitor resources during load testing:

```bash
# Monitor resource usage during load test
kubectl top pods -n todo-app --watch

# Monitor Kafka topic lag
kubectl exec -it my-cluster-kafka-0 -n kafka -- \
  bin/kafka-run-class.sh kafka.tools.ConsumerGroupCommand \
  --bootstrap-server localhost:9092 \
  --describe --group recurring-task-service-group
```

## Security Hardening

### Secrets Management
Ensure all sensitive information is properly managed:

```bash
# Rotate secrets regularly
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL=<new-db-url> \
  --from-literal=OPENAI_API_KEY=<new-api-key> \
  --from-literal=BETTER_AUTH_SECRET=<new-auth-secret> \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart deployments to pick up new secrets
kubectl rollout restart deployment/backend -n todo-app
kubectl rollout restart deployment/frontend -n todo-app
```

### Network Policies
Implement network policies to restrict traffic:

```yaml
# Example network policy to restrict traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: todo-app-policy
  namespace: todo-app
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kafka
    ports:
    - protocol: TCP
      port: 9092
```

## Maintenance Procedures

### Regular Maintenance Tasks
1. Monitor Kafka topic sizes and retention
2. Review and rotate secrets periodically
3. Update service images with security patches
4. Review and optimize resource allocations based on usage
5. Backup critical data regularly

### Backup and Recovery
```bash
# Backup Kafka topics (conceptual - actual implementation depends on setup)
# Use Kafka MirrorMaker or similar for cross-cluster replication

# Database backup (conceptual - actual implementation depends on Neon setup)
# Use Neon's built-in branching and point-in-time recovery features
```

This troubleshooting and optimization guide provides comprehensive information for maintaining the advanced cloud deployment system. Regular monitoring and optimization will ensure the system continues to perform well as usage grows.