#!/bin/bash

# Task ID: T345
# Test AI-assisted operations and document results

set -e  # Exit immediately if a command exits with a non-zero status

echo "Testing AI-assisted operations and documenting results..."

# Create a directory for AI operation logs
AI_LOG_DIR="phase-4/ai-operation-logs"
mkdir -p $AI_LOG_DIR

# Test Docker AI operations (if available)
echo "Testing Docker AI operations (if available)..."
if command -v docker &> /dev/null; then
    # Check if Gordon (Docker AI) is available
    if docker --help | grep -q "ai"; then
        echo "Docker AI (Gordon) is available. Testing commands..."
        
        # Test Dockerfile optimization
        echo "Testing Dockerfile optimization with Docker AI..."
        docker ai "optimize Dockerfile at phase-4/docker/frontend.Dockerfile" > "$AI_LOG_DIR/docker-ai-frontend-optimize.log" 2>&1 || echo "Docker AI command failed or not available" >> "$AI_LOG_DIR/docker-ai-frontend-optimize.log"
        
        docker ai "optimize Dockerfile at phase-4/docker/backend.Dockerfile" > "$AI_LOG_DIR/docker-ai-backend-optimize.log" 2>&1 || echo "Docker AI command failed or not available" >> "$AI_LOG_DIR/docker-ai-backend-optimize.log"
        
        docker ai "optimize Dockerfile at phase-4/docker/mcp-server.Dockerfile" > "$AI_LOG_DIR/docker-ai-mcp-optimize.log" 2>&1 || echo "Docker AI command failed or not available" >> "$AI_LOG_DIR/docker-ai-mcp-optimize.log"
        
        echo "✓ Docker AI operations completed (results in $AI_LOG_DIR)"
    else
        echo "Docker AI (Gordon) is not available in this environment"
        echo "Docker AI not available" > "$AI_LOG_DIR/docker-ai-status.log"
    fi
else
    echo "Docker is not available"
    echo "Docker not available" > "$AI_LOG_DIR/docker-status.log"
fi

# Test kubectl-ai operations (if available)
echo "Testing kubectl-ai operations (if available)..."
if command -v kubectl &> /dev/null; then
    # Check if kubectl-ai is available
    if kubectl --help | grep -q "ai\|-ai"; then
        echo "kubectl-ai is available. Testing commands..."
        
        # Test deployment verification
        echo "Testing deployment verification with kubectl-ai..."
        kubectl-ai "show status of all deployments in todo-app namespace" > "$AI_LOG_DIR/kubectl-ai-deployment-status.log" 2>&1 || echo "kubectl-ai command failed or not available" >> "$AI_LOG_DIR/kubectl-ai-deployment-status.log"
        
        # Test pod troubleshooting
        kubectl-ai "check why pods are failing in todo-app namespace" > "$AI_LOG_DIR/kubectl-ai-pod-troubleshoot.log" 2>&1 || echo "kubectl-ai command failed or not available" >> "$AI_LOG_DIR/kubectl-ai-pod-troubleshoot.log"
        
        # Test service creation
        kubectl-ai "create a deployment for a new service called analytics-service" > "$AI_LOG_DIR/kubectl-ai-create-deployment.log" 2>&1 || echo "kubectl-ai command failed or not available" >> "$AI_LOG_DIR/kubectl-ai-create-deployment.log"
        
        echo "✓ kubectl-ai operations completed (results in $AI_LOG_DIR)"
    else
        echo "kubectl-ai is not available in this environment"
        echo "kubectl-ai not available" > "$AI_LOG_DIR/kubectl-ai-status.log"
    fi
else
    echo "kubectl is not available"
    echo "kubectl not available" > "$AI_LOG_DIR/kubectl-status.log"
fi

# Test kagent operations (if available)
echo "Testing kagent operations (if available)..."
if command -v kagent &> /dev/null; then
    echo "kagent is available. Testing commands..."
    
    # Test cluster health analysis
    echo "Testing cluster health analysis with kagent..."
    kagent "analyze health of todo-app namespace" > "$AI_LOG_DIR/kagent-health-analysis.log" 2>&1 || echo "kagent command failed or not available" >> "$AI_LOG_DIR/kagent-health-analysis.log"
    
    # Test deployment troubleshooting
    kagent "why is my backend pod crashing in todo-app?" > "$AI_LOG_DIR/kagent-pod-troubleshoot.log" 2>&1 || echo "kagent command failed or not available" >> "$AI_LOG_DIR/kagent-pod-troubleshoot.log"
    
    # Test resource optimization
    kagent "optimize resource allocation for todo-app deployment" > "$AI_LOG_DIR/kagent-resource-optimization.log" 2>&1 || echo "kagent command failed or not available" >> "$AI_LOG_DIR/kagent-resource-optimization.log"
    
    echo "✓ kagent operations completed (results in $AI_LOG_DIR)"
else
    echo "kagent is not available in this environment"
    echo "kagent not available" > "$AI_LOG_DIR/kagent-status.log"
fi

# Document AI tool availability and test results
echo "Documenting AI tool availability and test results..."
cat > "$AI_LOG_DIR/ai-tools-summary.md" << EOF
# AI Tools Availability and Test Results

## Summary of AI Tool Testing

Date: $(date)

### Docker AI (Gordon)
Status: $(if command -v docker &> /dev/null && docker --help | grep -q "ai"; then echo "Available"; else echo "Not Available"; fi)

### kubectl-ai
Status: $(if command -v kubectl &> /dev/null && kubectl --help | grep -q "ai\|-ai"; then echo "Available"; else echo "Not Available"; fi)

### kagent
Status: $(if command -v kagent &> /dev/null; then echo "Available"; else echo "Not Available"; fi)

## Test Results

### Docker AI Operations
- Frontend Dockerfile optimization: $(if [ -f "$AI_LOG_DIR/docker-ai-frontend-optimize.log" ] && ! grep -q "not available" "$AI_LOG_DIR/docker-ai-frontend-optimize.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- Backend Dockerfile optimization: $(if [ -f "$AI_LOG_DIR/docker-ai-backend-optimize.log" ] && ! grep -q "not available" "$AI_LOG_DIR/docker-ai-backend-optimize.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- MCP Server Dockerfile optimization: $(if [ -f "$AI_LOG_DIR/docker-ai-mcp-optimize.log" ] && ! grep -q "not available" "$AI_LOG_DIR/docker-ai-mcp-optimize.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)

### kubectl-ai Operations
- Deployment status check: $(if [ -f "$AI_LOG_DIR/kubectl-ai-deployment-status.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kubectl-ai-deployment-status.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- Pod troubleshooting: $(if [ -f "$AI_LOG_DIR/kubectl-ai-pod-troubleshoot.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kubectl-ai-pod-troubleshoot.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- Deployment creation: $(if [ -f "$AI_LOG_DIR/kubectl-ai-create-deployment.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kubectl-ai-create-deployment.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)

### kagent Operations
- Health analysis: $(if [ -f "$AI_LOG_DIR/kagent-health-analysis.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kagent-health-analysis.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- Pod troubleshooting: $(if [ -f "$AI_LOG_DIR/kagent-pod-troubleshoot.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kagent-pod-troubleshoot.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)
- Resource optimization: $(if [ -f "$AI_LOG_DIR/kagent-resource-optimization.log" ] && ! grep -q "not available" "$AI_LOG_DIR/kagent-resource-optimization.log"; then echo "Completed"; else echo "Failed/Not Available"; fi)

## Recommendations

Based on the availability of AI tools in this environment:

$(if command -v docker &> /dev/null && docker --help | grep -q "ai"; then echo "1. Docker AI (Gordon) is available - use for Dockerfile optimization"; else echo "1. Docker AI (Gordon) is not available - consider installing for Docker optimization"; fi)

$(if command -v kubectl &> /dev/null && kubectl --help | grep -q "ai\|-ai"; then echo "2. kubectl-ai is available - use for Kubernetes operations"; else echo "2. kubectl-ai is not available - consider installing for Kubernetes assistance"; fi)

$(if command -v kagent &> /dev/null; then echo "3. kagent is available - use for cluster troubleshooting and optimization"; else echo "3. kagent is not available - consider installing for cluster management"; fi)

## Next Steps

1. Integrate available AI tools into deployment scripts where possible
2. Document specific use cases for each AI tool in the development workflow
3. Train team members on using available AI tools effectively
EOF

echo "AI-assisted operations testing completed!"
echo "Results documented in $AI_LOG_DIR/ai-tools-summary.md"
echo "Detailed logs available in $AI_LOG_DIR/"