#!/bin/bash
# Task ID: T312
# Script to deploy the application to Minikube using Helm

set -e  # Exit immediately if a command exits with a non-zero status

NAMESPACE="todo-app"

echo "Creating namespace if it doesn't exist..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "Creating secrets from environment variables..."
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  -n $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Installing Helm chart..."
helm install todo-app ./helm-charts/todo-app --namespace $NAMESPACE --create-namespace

echo "Checking deployment status..."
helm status todo-app -n $NAMESPACE

echo "Displaying pods..."
kubectl get pods -n $NAMESPACE

echo "Displaying services..."
kubectl get services -n $NAMESPACE

echo "Deployment completed successfully!"
echo "To access the frontend, run: minikube service frontend-service -n $NAMESPACE"