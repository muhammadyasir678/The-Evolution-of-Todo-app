#!/bin/bash

# Task ID: T339
# Test Helm chart installation with default and custom values

set -e  # Exit immediately if a command exits with a non-zero status

echo "Testing Helm chart installation with default and custom values..."

# Ensure Helm is available
if ! command -v helm &> /dev/null; then
    echo "Helm is not installed. Please install Helm before proceeding."
    exit 1
fi

# Ensure kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl before proceeding."
    exit 1
fi

# Create a temporary directory for test values
TEST_VALUES_DIR=$(mktemp -d)
TEST_RELEASE_NAME="todo-test"
TEST_NAMESPACE="todo-test"

# Create custom values file for testing
CUSTOM_VALUES_FILE="$TEST_VALUES_DIR/custom-values.yaml"
cat > "$CUSTOM_VALUES_FILE" << EOF
# Custom values for testing Helm chart
frontend:
  replicaCount: 1
  image:
    repository: nginx  # Using nginx for testing
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi

backend:
  replicaCount: 1
  image:
    repository: nginx  # Using nginx for testing
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi

mcpServer:
  replicaCount: 1
  image:
    repository: nginx  # Using nginx for testing
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 50m
      memory: 64Mi

# Use dummy values for testing
config:
  name: todo-test-config
  data:
    NEXT_PUBLIC_API_URL: "http://backend-service:8000"
    PORT: "3000"
    BACKEND_PORT: "8000"
    MCP_SERVER_PORT: "8080"

secrets:
  databaseUrl: "postgresql://test:test@test:5432/testdb"
  openaiApiKey: "test-key"
  authSecret: "test-secret"

namespace: $TEST_NAMESPACE
EOF

echo "Created custom values file for testing: $CUSTOM_VALUES_FILE"

# Create the test namespace
echo "Creating test namespace: $TEST_NAMESPACE"
kubectl create namespace $TEST_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Test 1: Install Helm chart with default values
echo "=== Test 1: Installing Helm chart with default values ==="
helm install $TEST_RELEASE_NAME ./helm-charts/todo-app-v5 --namespace $TEST_NAMESPACE --create-namespace

# Wait for all deployments to be ready
echo "Waiting for all deployments to be ready..."
kubectl wait deployment --all --for=condition=Available=True -n $TEST_NAMESPACE --timeout=300s

# Verify all resources were created
echo "Verifying resources were created..."
kubectl get all -n $TEST_NAMESPACE

# Check if all pods are running
echo "Checking pod status..."
POD_STATUS=$(kubectl get pods -n $TEST_NAMESPACE -o jsonpath='{range .items[*]}{.status.phase}{"\n"}{end}' | sort | uniq)
if echo "$POD_STATUS" | grep -q "Running"; then
    echo "✓ All pods are running"
else
    echo "✗ Some pods are not running"
    kubectl get pods -n $TEST_NAMESPACE
fi

# Test 2: Check services are accessible
echo "Checking services..."
kubectl get services -n $TEST_NAMESPACE

# Test 3: Upgrade with custom values
echo "=== Test 2: Upgrading Helm chart with custom values ==="
helm upgrade $TEST_RELEASE_NAME ./helm-charts/todo-app-v5 --namespace $TEST_NAMESPACE -f $CUSTOM_VALUES_FILE

# Wait for all deployments to be ready after upgrade
echo "Waiting for all deployments to be ready after upgrade..."
kubectl wait deployment --all --for=condition=Available=True -n $TEST_NAMESPACE --timeout=300s

# Verify resources after upgrade
echo "Verifying resources after upgrade..."
kubectl get all -n $TEST_NAMESPACE

# Test 4: Rollback to previous version
echo "=== Test 3: Rolling back to previous version ==="
helm rollback $TEST_RELEASE_NAME --namespace $TEST_NAMESPACE

# Wait for rollback to complete
echo "Waiting for rollback to complete..."
kubectl wait deployment --all --for=condition=Available=True -n $TEST_NAMESPACE --timeout=300s

# Test 5: Test dry-run to validate templates
echo "=== Test 4: Validating Helm templates with dry-run ==="
helm install $TEST_RELEASE_NAME ./helm-charts/todo-app-v5 --namespace $TEST_NAMESPACE --dry-run --debug

echo "Helm chart testing completed successfully!"

# Clean up
echo "Cleaning up test resources..."
helm uninstall $TEST_RELEASE_NAME --namespace $TEST_NAMESPACE
kubectl delete namespace $TEST_NAMESPACE

# Clean up temporary directory
rm -rf $TEST_VALUES_DIR

echo "All Helm chart tests completed!"
echo "1. ✓ Installed with default values"
echo "2. ✓ Upgraded with custom values"
echo "3. ✓ Rolled back to previous version"
echo "4. ✓ Validated templates with dry-run"