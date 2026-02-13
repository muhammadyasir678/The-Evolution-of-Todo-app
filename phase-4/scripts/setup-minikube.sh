#!/bin/bash

# Task ID: T320
# Setup Minikube environment with proper installation steps and cluster start

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Minikube environment for Todo App deployment..."

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Installing Minikube..."
    case $(uname -s) in
        Linux*)
            # For Linux
            curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
            sudo install minikube-linux-amd64 /usr/local/bin/minikube
            ;;
        Darwin*)
            # For macOS
            brew install minikube
            ;;
        *)
            echo "Unsupported OS. Please install Minikube manually."
            exit 1
            ;;
    esac
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl before proceeding."
    exit 1
fi

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "Helm is not installed. Installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
fi

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker before proceeding."
    exit 1
fi

# Start Minikube with sufficient resources for the application
echo "Starting Minikube cluster with 4 CPUs and 8GB memory..."
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Enable required addons
echo "Enabling required Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Verify Minikube is running
echo "Verifying Minikube status..."
minikube status

echo "Minikube environment setup completed successfully!"
echo "Cluster is ready for application deployment."