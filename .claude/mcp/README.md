# MCP Server for Todo App Development

This MCP (Multi-Agent Collaboration Protocol) server provides integrated capabilities for developing the Todo application. The server enables various development operations through standardized interfaces.

## Capabilities

### Filesystem Operations
- `mcp.fs.read`: Read files from the filesystem
- `mcp.fs.write`: Write content to files
- `mcp.fs.list`: List files in a directory
- `mcp.fs.create_dir`: Create directories
- `mcp.fs.delete`: Delete files or directories

### GitHub Operations
- `mcp.github.clone`: Clone repositories
- `mcp.github.commit`: Commit changes
- `mcp.github.push`: Push changes to remote

### PostgreSQL Operations
- `mcp.postgres.connect`: Connect to database
- `mcp.postgres.query`: Execute SELECT queries
- `mcp.postgres.execute`: Execute non-SELECT queries

### HTTP Operations (Fetch)
- `mcp.fetch.get`: HTTP GET requests
- `mcp.fetch.post`: HTTP POST requests
- `mcp.fetch.put`: HTTP PUT requests
- `mcp.fetch.delete`: HTTP DELETE requests

### Docker Operations
- `mcp.docker.build`: Build Docker images
- `mcp.docker.run`: Run containers
- `mcp.docker.push`: Push images to registry
- `mcp.docker.status`: Check container status

### Web Search (Brave Search)
- `mcp.search.web`: Perform web searches (requires BRAVE_API_KEY)

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r .claude/mcp/requirements.txt
   ```

2. Set up environment variables if needed:
   ```bash
   export BRAVE_API_KEY=your_brave_api_key_here
   ```

## Running the Server

Start the server using the provided script:
```bash
./.claude/mcp/start.sh
```

Or run directly:
```bash
python .claude/mcp/server.py
```

## Integration with Claude Code

This MCP server integrates with Claude Code's capabilities, allowing the AI assistant to perform various development tasks programmatically. The server runs on localhost:8080 by default.

## Configuration

The server configuration is located at `.claude/mcp/config.json`. You can modify this file to adjust capabilities, endpoints, and settings.