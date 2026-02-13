#!/bin/bash

# Task ID: T333
# Validate Kubernetes manifests follow best practices for production readiness

set -e  # Exit immediately if a command exits with a non-zero status

echo "Validating Kubernetes manifests for best practices..."

# Check if kubeval is installed, install if not
if ! command -v kubeval &> /dev/null; then
    echo "Installing kubeval for Kubernetes manifest validation..."
    # For Linux
    wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
    tar xf kubeval-linux-amd64.tar.gz
    sudo cp kubeval /usr/local/bin
    rm kubeval-linux-amd64.tar.gz
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl before proceeding."
    exit 1
fi

# Validate all Kubernetes manifests
echo "Validating Kubernetes manifests in k8s/ directory..."
for file in k8s/*.yaml; do
    if [[ -f "$file" ]]; then
        echo "Validating $file..."
        kubeval --strict --ignore-missing-schemas "$file"
        if [ $? -eq 0 ]; then
            echo "✓ $file is valid"
        else
            echo "✗ $file has validation errors"
        fi
    fi
done

# Check for best practices in the manifests
echo "Checking for Kubernetes best practices..."

# Check 1: Ensure resource limits and requests are set
echo "Checking for resource limits and requests..."
for file in k8s/*.yaml; do
    if [[ -f "$file" ]]; then
        if grep -q "kind: Deployment" "$file"; then
            if ! grep -A 10 "resources:" "$file" | grep -q "requests\|limits"; then
                echo "⚠️  $file: Missing resource limits/requests in deployment"
            else
                echo "✓ $file: Resources properly configured"
            fi
        fi
    fi
done

# Check 2: Ensure health checks are present
echo "Checking for health checks..."
for file in k8s/*.yaml; do
    if [[ -f "$file" ]]; then
        if grep -q "kind: Deployment" "$file"; then
            if ! grep -q "livenessProbe\|readinessProbe" "$file"; then
                echo "⚠️  $file: Missing health checks in deployment"
            else
                echo "✓ $file: Health checks present"
            fi
        fi
    fi
done

# Check 3: Ensure proper security contexts
echo "Checking for security contexts..."
for file in k8s/*.yaml; do
    if [[ -f "$file" ]]; then
        if grep -q "kind: Deployment" "$file"; then
            if ! grep -q "securityContext\|runAsNonRoot\|readOnlyRootFilesystem" "$file"; then
                echo "⚠️  $file: Missing security context in deployment"
            else
                echo "✓ $file: Security context present"
            fi
        fi
    fi
done

# Check 4: Ensure proper labels and selectors
echo "Checking for proper labels and selectors..."
for file in k8s/*.yaml; do
    if [[ -f "$file" ]]; then
        if grep -q "kind: Deployment\|kind: Service" "$file"; then
            if ! grep -q "app:\|name:" "$file"; then
                echo "⚠️  $file: Missing proper labels/selectors"
            else
                echo "✓ $file: Proper labels/selectors present"
            fi
        fi
    fi
done

# Check 5: Verify Dapr annotations are present where needed
echo "Checking for Dapr annotations..."
for file in k8s/services/*.yaml; do
    if [[ -f "$file" ]]; then
        if grep -q "kind: Deployment" "$file"; then
            if ! grep -q "dapr.io/app-id\|dapr.io/enabled" "$file"; then
                echo "⚠️  $file: Missing Dapr annotations in deployment"
            else
                echo "✓ $file: Dapr annotations present"
            fi
        fi
    fi
done

echo "Kubernetes manifest validation completed!"
echo "Note: This script performs basic validation. For comprehensive validation, consider using tools like:"
echo "- Datree (https://datree.io/) for policy enforcement"
echo "- Conftest (https://www.conftest.dev/) for policy validation"
echo "- Kubesec (https://kubesec.io/) for security scanning"