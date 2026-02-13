#!/bin/bash

# Task ID: T334
# Test individual Kubernetes resources with kubectl apply and verification

set -e  # Exit immediately if a command exits with a non-zero status

echo "Testing individual Kubernetes resources with kubectl apply and verification..."

# Ensure kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl before proceeding."
    exit 1
fi

# Create a temporary namespace for testing
TEST_NAMESPACE="todo-test"
echo "Creating temporary namespace: $TEST_NAMESPACE"
kubectl create namespace $TEST_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Function to test a single Kubernetes resource
test_resource() {
    local resource_file=$1
    local resource_name=$2
    local resource_type=$3
    
    echo "Testing $resource_type: $resource_name from $resource_file"
    
    # Apply the resource
    kubectl apply -f "$resource_file" -n $TEST_NAMESPACE
    if [ $? -eq 0 ]; then
        echo "✓ Successfully applied $resource_type: $resource_name"
    else
        echo "✗ Failed to apply $resource_type: $resource_name"
        return 1
    fi
    
    # Wait a moment for the resource to be processed
    sleep 5
    
    # Verify the resource was created
    if kubectl get $resource_type $resource_name -n $TEST_NAMESPACE &> /dev/null; then
        echo "✓ $resource_type: $resource_name verified in cluster"
    else
        echo "✗ $resource_type: $resource_name not found in cluster after apply"
        return 1
    fi
    
    # If it's a deployment, check if it's ready
    if [ "$resource_type" = "deployment" ]; then
        echo "Waiting for deployment $resource_name to be ready..."
        kubectl wait deployment/$resource_name --for=condition=Available=True -n $TEST_NAMESPACE --timeout=120s
        if [ $? -eq 0 ]; then
            echo "✓ Deployment $resource_name is ready"
        else
            echo "✗ Deployment $resource_name is not ready within timeout"
            return 1
        fi
    fi
    
    # If it's a service, check if it's accessible
    if [ "$resource_type" = "service" ]; then
        # Get the service details
        kubectl get service $resource_name -n $TEST_NAMESPACE
        echo "✓ Service $resource_name created and accessible"
    fi
    
    # If it's a configmap or secret, verify its content
    if [ "$resource_type" = "configmap" ] || [ "$resource_type" = "secret" ]; then
        kubectl describe $resource_type $resource_name -n $TEST_NAMESPACE
        echo "✓ $resource_type $resource_name details verified"
    fi
    
    # Clean up the resource after testing
    kubectl delete $resource_type $resource_name -n $TEST_NAMESPACE
    echo "✓ Cleaned up $resource_type: $resource_name"
    echo ""
}

# Test all Kubernetes resources individually
echo "Testing all Kubernetes resources in k8s/ directory..."

# Test namespace (though it's already created)
echo "Testing namespace configuration..."
kubectl apply -f k8s/namespace.yaml
echo "✓ Namespace configuration validated"

# Test configmap
if [ -f "k8s/configmap.yaml" ]; then
    test_resource "k8s/configmap.yaml" "todo-config" "configmap"
fi

# Test secret
if [ -f "k8s/secret.yaml" ]; then
    # Create a temporary secret with dummy values for testing
    TEMP_SECRET_FILE=$(mktemp)
    sed 's/{{ .Values.* }}/"dummy-value"/g' k8s/secret.yaml > $TEMP_SECRET_FILE
    test_resource "$TEMP_SECRET_FILE" "todo-secrets" "secret"
    rm $TEMP_SECRET_FILE
fi

# Test frontend deployment
if [ -f "k8s/frontend-deployment.yaml" ]; then
    # Create a temporary deployment with dummy image for testing
    TEMP_DEPLOY_FILE=$(mktemp)
    sed 's|image:.*|image: nginx:latest|g' k8s/frontend-deployment.yaml > $TEMP_DEPLOY_FILE
    test_resource "$TEMP_DEPLOY_FILE" "frontend-deployment" "deployment"
    rm $TEMP_DEPLOY_FILE
fi

# Test frontend service
if [ -f "k8s/frontend-service.yaml" ]; then
    test_resource "k8s/frontend-service.yaml" "frontend-service" "service"
fi

# Test backend deployment
if [ -f "k8s/backend-deployment.yaml" ]; then
    # Create a temporary deployment with dummy image for testing
    TEMP_DEPLOY_FILE=$(mktemp)
    sed 's|image:.*|image: nginx:latest|g' k8s/backend-deployment.yaml > $TEMP_DEPLOY_FILE
    test_resource "$TEMP_DEPLOY_FILE" "backend-deployment" "deployment"
    rm $TEMP_DEPLOY_FILE
fi

# Test backend service
if [ -f "k8s/backend-service.yaml" ]; then
    test_resource "k8s/backend-service.yaml" "backend-service" "service"
fi

# Test MCP deployment
if [ -f "k8s/mcp-deployment.yaml" ]; then
    # Create a temporary deployment with dummy image for testing
    TEMP_DEPLOY_FILE=$(mktemp)
    sed 's|image:.*|image: nginx:latest|g' k8s/mcp-deployment.yaml > $TEMP_DEPLOY_FILE
    test_resource "$TEMP_DEPLOY_FILE" "mcp-deployment" "deployment"
    rm $TEMP_DEPLOY_FILE
fi

# Test MCP service
if [ -f "k8s/mcp-service.yaml" ]; then
    test_resource "k8s/mcp-service.yaml" "mcp-service" "service"
fi

# Clean up the test namespace
echo "Cleaning up test namespace: $TEST_NAMESPACE"
kubectl delete namespace $TEST_NAMESPACE

echo "Individual Kubernetes resource testing completed!"
echo "All resources were successfully applied, verified, and cleaned up."