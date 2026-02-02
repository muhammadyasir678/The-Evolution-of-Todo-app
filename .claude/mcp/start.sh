#!/bin/bash

# Start the MCP server for the Todo app development
echo "Starting MCP Server for Todo app..."

# Change to the project directory
cd "$(dirname "$0")/../.."

# Install dependencies
pip install -r .claude/mcp/requirements.txt

# Start the server
python .claude/mcp/server.py