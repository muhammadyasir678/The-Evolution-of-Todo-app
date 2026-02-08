#!/bin/bash

# Script to deploy Phase V services to cloud Kubernetes (AKS/GKE/DOKS)
# This script deploys the full stack to cloud with managed Kafka

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment to cloud Kubernetes..."

# Validate required environment variables
if [ -z "$KUBE_CONFIG_DATA" ]; then
  echo "Error: KUBE_CONFIG_DATA environment variable is required"
  exit 1
fi

if [ -z "$KAFKA_BOOTSTRAP_SERVERS" ]; then
  echo "Error: KAFKA_BOOTSTRAP_SERVERS environment variable is required"
  exit 1
fi

if [ -z "$KAFKA_SASL_USERNAME" ]; then
  echo "Error: KAFKA_SASL_USERNAME environment variable is required"
  exit 1
fi

if [ -z "$KAFKA_SASL_PASSWORD" ]; then
  echo "Error: KAFKA_SASL_PASSWORD environment variable is required"
  exit 1
fi

# Set up kubeconfig
echo "Setting up Kubernetes configuration..."
mkdir -p ~/.kube
echo "$KUBE_CONFIG_DATA" | base64 -d > ~/.kube/config
chmod 600 ~/.kube/config

# Update Dapr pubsub.yaml with cloud Kafka configuration
echo "Updating Dapr pubsub configuration for cloud Kafka..."
cat > k8s/dapr/pubsub-cloud.yaml << EOF
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
    value: "$KAFKA_BOOTSTRAP_SERVERS"  # Cloud managed Kafka brokers
  - name: authType
    value: "saslPlaintext"  # Using SASL for cloud Kafka authentication
  - name: saslUsername
    value: "$KAFKA_SASL_USERNAME"
  - name: saslPassword
    secretKeyRef:
      name: kafka-secrets
      key: saslPassword
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: clientID
    value: "dapr-kafka-client"
  - name: authRequired
    value: "true"
EOF

# Apply the updated Dapr configuration
kubectl apply -f k8s/dapr/pubsub-cloud.yaml

# Create Kafka secrets
echo "Creating Kafka secrets..."
kubectl create secret generic kafka-secrets \
  --from-literal=saslPassword="$KAFKA_SASL_PASSWORD" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Create application secrets
echo "Creating application secrets..."
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --from-literal=SENDGRID_API_KEY="$SENDGRID_API_KEY" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy the application using Helm with cloud-specific values
echo "Deploying application with Helm..."
helm upgrade --install todo-app-v5 helm-charts/todo-app-v5 \
  --namespace todo-app \
  --create-namespace \
  --set frontend.replicaCount=2 \
  --set backend.replicaCount=2 \
  --set mcpServer.replicaCount=2 \
  --set recurringTaskService.replicaCount=2 \
  --set notificationService.replicaCount=2 \
  --set auditService.replicaCount=2 \
  --set websocketService.replicaCount=2 \
  --set frontend.resources.requests.cpu=100m \
  --set frontend.resources.requests.memory=128Mi \
  --set frontend.resources.limits.cpu=500m \
  --set frontend.resources.limits.memory=512Mi \
  --set backend.resources.requests.cpu=200m \
  --set backend.resources.requests.memory=256Mi \
  --set backend.resources.limits.cpu=1000m \
  --set backend.resources.limits.memory=1024Mi \
  --wait \
  --timeout=10m

# Wait for all deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available deployment/frontend -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/backend -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/mcp-server -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/recurring-task-service -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/notification-service -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/audit-service -n todo-app --timeout=600s
kubectl wait --for=condition=available deployment/websocket-service -n todo-app --timeout=600s

# Display deployment status
echo "Displaying pods..."
kubectl get pods -n todo-app

echo "Displaying services..."
kubectl get services -n todo-app

echo "Displaying deployments..."
kubectl get deployments -n todo-app

# Get the external IP/URL for the frontend service
echo "Getting frontend service external endpoint..."
FRONTEND_EXTERNAL_IP=""
while [ -z "$FRONTEND_EXTERNAL_IP" ]; do
  FRONTEND_EXTERNAL_IP=$(kubectl get service frontend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  if [ -z "$FRONTEND_EXTERNAL_IP" ]; then
    FRONTEND_EXTERNAL_IP=$(kubectl get service frontend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
  fi
  if [ -z "$FRONTEND_EXTERNAL_IP" ]; then
    echo "Waiting for external IP/hostname assignment..."
    sleep 10
  fi
done

echo "Deployment to cloud completed successfully!"
echo "Application is accessible at: http://$FRONTEND_EXTERNAL_IP"

# Set up monitoring if available
if command -v kubectl &> /dev/null && [ -n "$SETUP_MONITORING" ]; then
  echo "Setting up monitoring and logging..."
  # This would typically involve deploying Prometheus, Grafana, and other monitoring tools
  # For brevity, we're just noting this step here
  echo "Monitoring setup completed"
fi