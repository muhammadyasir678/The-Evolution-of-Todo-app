# Azure (AKS) Deployment Script
# This script prepares and deploys the application to Azure Kubernetes Service

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting deployment to Azure Kubernetes Service (AKS)..."

# Login to Azure (you'll need to have Azure CLI installed and logged in)
# az login

# Set your resource group and cluster name
RESOURCE_GROUP=${RESOURCE_GROUP:-"todo-app-rg"}
CLUSTER_NAME=${CLUSTER_NAME:-"todo-app-aks"}
LOCATION=${LOCATION:-"eastus"}

echo "Using Resource Group: $RESOURCE_GROUP"
echo "Using Cluster Name: $CLUSTER_NAME"
echo "Using Location: $LOCATION"

# Create resource group if it doesn't exist
echo "Checking if resource group exists..."
if ! az group show --name $RESOURCE_GROUP --out none 2>/dev/null; then
    echo "Creating resource group: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION
fi

# Create AKS cluster if it doesn't exist
echo "Checking if AKS cluster exists..."
if ! az aks show --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --out none 2>/dev/null; then
    echo "Creating AKS cluster: $CLUSTER_NAME"
    az aks create \
        --resource-group $RESOURCE_GROUP \
        --name $CLUSTER_NAME \
        --node-count 3 \
        --enable-addons monitoring \
        --generate-ssh-keys \
        --enable-managed-identity
fi

# Get AKS credentials
echo "Getting AKS credentials..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME

# Verify connection to AKS
echo "Verifying connection to AKS..."
kubectl cluster-info

# Install Dapr on AKS
echo "Installing Dapr on AKS..."
dapr init -k --wait

# Create namespace if it doesn't exist
echo "Creating todo-app namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# For Redpanda Cloud, we don't deploy Kafka locally
# Instead, we rely on the external managed service
echo "Using Redpanda Cloud as managed Kafka service (external to AKS)"
# In a real scenario, you would ensure the topics exist in Redpanda Cloud
# This could be done via Redpanda Cloud API or CLI

# Apply Dapr components for AKS
echo "Applying Dapr components to AKS..."
kubectl apply -f k8s/dapr/config.yaml
# For production with Redpanda Cloud, use the cloud configuration
kubectl apply -f k8s/dapr/pubsub-redpanda-cloud.yaml
kubectl apply -f k8s/dapr/statestore.yaml
kubectl apply -f k8s/dapr/secretstore.yaml
kubectl apply -f k8s/dapr/bindings.cron.yaml
kubectl apply -f k8s/dapr/reminder-cron-binding.yaml
kubectl apply -f k8s/dapr/backend-reminder-subscription.yaml

# Create Redpanda Cloud secrets (these need to be configured with actual values)
echo "Creating Redpanda Cloud secrets (configure with actual values)..."
kubectl create secret generic redpanda-cloud-secrets \
  --from-literal=username="${REDPANDA_USERNAME:-your_redpanda_username}" \
  --from-literal=password="${REDPANDA_PASSWORD:-your_redpanda_password}" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Create secrets for the application on AKS
echo "Creating application secrets on AKS..."
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="${DATABASE_URL:-postgresql://username:password@neon-host.region.provider.neon.tech/dbname}" \
  --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY:-your_openai_api_key}" \
  --from-literal=BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET:-your_auth_secret}" \
  --from-literal=SENDGRID_API_KEY="${SENDGRID_API_KEY:-your_sendgrid_api_key}" \
  -n todo-app \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy the application using Helm to AKS
echo "Deploying application to AKS with Helm..."
helm upgrade --install todo-app-v5 helm-charts/todo-app-v5 --namespace todo-app --create-namespace

# Wait for all deployments to be ready
echo "Waiting for deployments to be ready on AKS..."
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=600s
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=600s
kubectl wait --for=condition=ready pod -l app=recurring-task-service -n todo-app --timeout=600s
kubectl wait --for=condition=ready pod -l app=notification-service -n todo-app --timeout=600s
kubectl wait --for=condition=ready pod -l app=audit-service -n todo-app --timeout=600s
kubectl wait --for=condition=ready pod -l app=websocket-service -n todo-app --timeout=600s

# Display deployment status
echo "Displaying pods on AKS..."
kubectl get pods -n todo-app

echo "Displaying services on AKS..."
kubectl get services -n todo-app

echo "Displaying deployments on AKS..."
kubectl get deployments -n todo-app

echo "Deployment to Azure Kubernetes Service completed successfully!"
echo "Access the frontend using the external IP from: kubectl get services -n todo-app"