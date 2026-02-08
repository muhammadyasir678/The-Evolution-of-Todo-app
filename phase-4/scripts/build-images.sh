#!/bin/bash
# Task ID: T311
# Script to build Docker images in Minikube environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting Docker environment to use Minikube's Docker daemon..."
eval $(minikube docker-env)

echo "Building frontend Docker image..."
docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../../phase-3/frontend

echo "Building backend Docker image..."
docker build -t todo-backend:latest -f docker/backend.Dockerfile ../../phase-3/backend

echo "Building MCP server Docker image..."
docker build -t todo-mcp-server:latest -f docker/mcp-server.Dockerfile ../../phase-3/mcp-server

echo "Verifying images were built..."
docker images | grep todo

echo "Build completed successfully!"