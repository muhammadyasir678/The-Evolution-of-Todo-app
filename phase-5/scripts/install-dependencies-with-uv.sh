#!/bin/bash

# Script to install dependencies using uv for all Phase V services
# This script demonstrates the use of uv for fast dependency installation

set -e  # Exit immediately if a command exits with a non-zero status

echo "Installing dependencies with uv for Phase V services..."

# Function to install dependencies for a project
install_with_uv() {
    local project_dir=$1
    local project_name=$2
    
    echo "Installing dependencies for $project_name..."
    cd "$project_dir"
    
    # If pyproject.toml exists, use uv sync
    if [ -f "pyproject.toml" ]; then
        echo "Using pyproject.toml to install dependencies with uv..."
        uv sync --locked
    elif [ -f "requirements.txt" ]; then
        echo "Using requirements.txt to install dependencies with uv..."
        uv pip install -r requirements.txt
    else
        echo "No pyproject.toml or requirements.txt found in $project_dir"
    fi
    
    cd - > /dev/null
    echo "Successfully installed dependencies for $project_name"
    echo ""
}

# Install backend dependencies
install_with_uv "/mnt/f/The-Evolution-of-Todo-app/phase-5/backend" "Backend Service"

# Install recurring task service dependencies
install_with_uv "/mnt/f/The-Evolution-of-Todo-app/phase-5/services/recurring-task-service" "Recurring Task Service"

# Install notification service dependencies
install_with_uv "/mnt/f/The-Evolution-of-Todo-app/phase-5/services/notification-service" "Notification Service"

# Install audit service dependencies
install_with_uv "/mnt/f/The-Evolution-of-Todo-app/phase-5/services/audit-service" "Audit Service"

# Install websocket service dependencies
install_with_uv "/mnt/f/The-Evolution-of-Todo-app/phase-5/services/websocket-service" "WebSocket Service"

echo "All dependencies installed successfully with uv!"
echo ""
echo "To activate a virtual environment with the dependencies:"
echo "  cd <service-directory>"
echo "  uv venv  # Creates a virtual environment"
echo "  source .venv/bin/activate  # Activates the environment"
echo ""
echo "To add new dependencies:"
echo "  uv add <package-name>  # If using pyproject.toml"
echo "  Or add to requirements.txt and run: uv pip install -r requirements.txt"