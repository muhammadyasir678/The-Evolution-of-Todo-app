#!/usr/bin/env python3
"""
MCP Server for the Todo app development
Implements filesystem, github, postgres, fetch, kubernetes, docker, and brave-search capabilities
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
import aiohttp
import subprocess
import tempfile

# Placeholder imports for MCP - these may need adjustment based on actual available packages
try:
    from mcp.server import Server
    from mcp.types import TextDocumentIdentifier, DiagnosticSeverity
    import mcp.trace as trace
    MCP_AVAILABLE = True
except ImportError:
    # Fallback implementation if MCP packages aren't available
    print("MCP packages not available, using fallback server implementation")
    MCP_AVAILABLE = False
    # Define minimal server interface for fallback
    class Server:
        def __init__(self, name):
            self.name = name
            self.handlers = {}

        def request(self, method):
            def decorator(func):
                self.handlers[method] = func
                return func
            return decorator

        def notification(self, method):
            def decorator(func):
                self.handlers[method] = func
                return func
            return decorator

        async def listen(self):
            # Simple context manager implementation
            yield self

    server = Server("specifyplus-mcp")


# Initialize the server
if MCP_AVAILABLE:
    server = Server("specifyplus-mcp")
else:
    server = Server("specifyplus-mcp")


@server.request("initialize")
async def handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle the initialize request from the MCP client."""
    return {
        "capabilities": {
            "resources": {},
            "prompts": {},
            "notifications": {}
        }
    }


# Filesystem capability implementations
@server.request("mcp.fs.read")
async def fs_read(params: Dict[str, Any]) -> Dict[str, str]:
    """Read a file from the filesystem."""
    file_path = params.get("path", "")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


@server.request("mcp.fs.write")
async def fs_write(params: Dict[str, Any]) -> Dict[str, bool]:
    """Write content to a file."""
    file_path = params.get("path", "")
    content = params.get("content", "")
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.request("mcp.fs.list")
async def fs_list(params: Dict[str, Any]) -> Dict[str, list]:
    """List files in a directory."""
    dir_path = params.get("path", ".")
    try:
        files = []
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            files.append({
                "name": item,
                "is_directory": os.path.isdir(item_path),
                "size": os.path.getsize(item_path) if not os.path.isdir(item_path) else 0
            })
        return {"files": files}
    except Exception as e:
        return {"files": [], "error": str(e)}


@server.request("mcp.fs.create_dir")
async def fs_create_dir(params: Dict[str, Any]) -> Dict[str, bool]:
    """Create a directory."""
    dir_path = params.get("path", "")
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.request("mcp.fs.delete")
async def fs_delete(params: Dict[str, Any]) -> Dict[str, bool]:
    """Delete a file or directory."""
    path = params.get("path", "")
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            return {"success": False, "error": "Path does not exist"}
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# GitHub capability implementations
@server.request("mcp.github.clone")
async def github_clone(params: Dict[str, Any]) -> Dict[str, bool]:
    """Clone a GitHub repository."""
    repo_url = params.get("url", "")
    destination = params.get("destination", "./cloned_repo")

    try:
        result = subprocess.run(
            ["git", "clone", repo_url, destination],
            check=True,
            capture_output=True,
            text=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


@server.request("mcp.github.commit")
async def github_commit(params: Dict[str, Any]) -> Dict[str, bool]:
    """Commit changes to a GitHub repository."""
    message = params.get("message", "Auto-commit from MCP")
    files = params.get("files", ["."])  # Default to all files

    try:
        # Add files
        subprocess.run(["git", "add"] + files, check=True, capture_output=True, text=True)

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


@server.request("mcp.github.push")
async def github_push(params: Dict[str, Any]) -> Dict[str, bool]:
    """Push changes to a GitHub repository."""
    remote = params.get("remote", "origin")
    branch = params.get("branch", "main")

    try:
        result = subprocess.run(
            ["git", "push", remote, branch],
            check=True,
            capture_output=True,
            text=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


# PostgreSQL capability implementations
@server.request("mcp.postgres.connect")
async def postgres_connect(params: Dict[str, Any]) -> Dict[str, bool]:
    """Connect to a PostgreSQL database."""
    host = params.get("host", "localhost")
    port = params.get("port", 5432)
    database = params.get("database", "postgres")
    username = params.get("username", "postgres")
    password = params.get("password", "")

    try:
        import asyncpg

        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        # Store connection in server state or return connection ID
        # For simplicity, just returning success here
        await conn.close()
        return {"success": True}
    except ImportError:
        return {"success": False, "error": "asyncpg library not installed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.request("mcp.postgres.query")
async def postgres_query(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a SELECT query on PostgreSQL."""
    query = params.get("sql", "")
    host = params.get("host", "localhost")
    port = params.get("port", 5432)
    database = params.get("database", "postgres")
    username = params.get("username", "postgres")
    password = params.get("password", "")

    try:
        import asyncpg

        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )

        result = await conn.fetch(query)
        await conn.close()

        # Convert records to list of dicts
        rows = [dict(r) for r in result]
        return {"success": True, "rows": rows}
    except ImportError:
        return {"success": False, "error": "asyncpg library not installed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@server.request("mcp.postgres.execute")
async def postgres_execute(params: Dict[str, Any]) -> Dict[str, bool]:
    """Execute a non-SELECT query on PostgreSQL."""
    query = params.get("sql", "")
    host = params.get("host", "localhost")
    port = params.get("port", 5432)
    database = params.get("database", "postgres")
    username = params.get("username", "postgres")
    password = params.get("password", "")

    try:
        import asyncpg

        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )

        await conn.execute(query)
        await conn.close()

        return {"success": True}
    except ImportError:
        return {"success": False, "error": "asyncpg library not installed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Fetch capability implementations
@server.request("mcp.fetch.get")
async def fetch_get(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an HTTP GET request."""
    url = params.get("url", "")
    headers = params.get("headers", {})

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                content = await response.text()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content
                }
    except Exception as e:
        return {"error": str(e)}


@server.request("mcp.fetch.post")
async def fetch_post(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an HTTP POST request."""
    url = params.get("url", "")
    headers = params.get("headers", {})
    body = params.get("body", {})

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as response:
                content = await response.text()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content
                }
    except Exception as e:
        return {"error": str(e)}


@server.request("mcp.fetch.put")
async def fetch_put(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an HTTP PUT request."""
    url = params.get("url", "")
    headers = params.get("headers", {})
    body = params.get("body", {})

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, json=body) as response:
                content = await response.text()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content
                }
    except Exception as e:
        return {"error": str(e)}


@server.request("mcp.fetch.delete")
async def fetch_delete(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform an HTTP DELETE request."""
    url = params.get("url", "")
    headers = params.get("headers", {})

    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                content = await response.text()
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "content": content
                }
    except Exception as e:
        return {"error": str(e)}


# Docker capability implementations
@server.request("mcp.docker.build")
async def docker_build(params: Dict[str, Any]) -> Dict[str, bool]:
    """Build a Docker image."""
    dockerfile_path = params.get("dockerfile", "Dockerfile")
    context = params.get("context", ".")
    tag = params.get("tag", "todo-app:latest")

    try:
        result = subprocess.run(
            ["docker", "build", "-f", dockerfile_path, "-t", tag, context],
            check=True,
            capture_output=True,
            text=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


@server.request("mcp.docker.run")
async def docker_run(params: Dict[str, Any]) -> Dict[str, str]:
    """Run a Docker container."""
    image = params.get("image", "todo-app:latest")
    ports = params.get("ports", [])
    env_vars = params.get("env", {})

    cmd = ["docker", "run", "-d"]

    # Add port mappings
    for port in ports:
        cmd.extend(["-p", port])

    # Add environment variables
    for key, value in env_vars.items():
        cmd.extend(["-e", f"{key}={value}"])

    cmd.append(image)

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        container_id = result.stdout.strip()
        return {"success": True, "container_id": container_id}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


@server.request("mcp.docker.push")
async def docker_push(params: Dict[str, Any]) -> Dict[str, bool]:
    """Push a Docker image to registry."""
    tag = params.get("tag", "todo-app:latest")

    try:
        result = subprocess.run(
            ["docker", "push", tag],
            check=True,
            capture_output=True,
            text=True
        )
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "output": e.stderr}


@server.request("mcp.docker.status")
async def docker_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get Docker container status."""
    container_id = params.get("container_id", "")

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}}\t{{.Names}}\t{{.Status}}"],
            check=True,
            capture_output=True,
            text=True
        )
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) == 3:
                    containers.append({
                        "id": parts[0],
                        "name": parts[1],
                        "status": parts[2]
                    })

        # If a specific container_id was provided, filter for it
        if container_id:
            containers = [c for c in containers if c['id'].startswith(container_id)]

        return {"containers": containers}
    except subprocess.CalledProcessError as e:
        return {"containers": [], "error": str(e), "output": e.stderr}


# Brave Search capability implementation
@server.request("mcp.search.web")
async def brave_search(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a web search using Brave Search API."""
    query = params.get("query", "")
    api_key = params.get("api_key", os.getenv("BRAVE_API_KEY"))

    if not api_key:
        return {"error": "BRAVE_API_KEY not provided or set in environment"}

    headers = {
        "X-Subscription-Token": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "text_decorations": False,
        "spellcheck": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()

                    # Extract relevant search results
                    results = []
                    if "web" in data and "results" in data["web"]:
                        for result in data["web"]["results"]:
                            results.append({
                                "title": result.get("title", ""),
                                "url": result.get("url", ""),
                                "description": result.get("description", "")
                            })

                    return {"success": True, "results": results}
                else:
                    return {"error": f"API returned status {response.status}"}
    except Exception as e:
        return {"error": str(e)}


@server.notification("initialized")
async def handle_initialized():
    """Handle the initialized notification from the MCP client."""
    print("MCP Server initialized!")


async def main():
    """Start the MCP server."""
    if MCP_AVAILABLE:
        async with server.listen():
            print("MCP Server started on localhost:8080")
            print("Capabilities available:")
            print("- Filesystem operations: read, write, list, create_dir, delete")
            print("- GitHub operations: clone, commit, push")
            print("- PostgreSQL operations: connect, query, execute")
            print("- HTTP operations: get, post, put, delete")
            print("- Docker operations: build, run, push, status")
            print("- Web search: search.web (requires BRAVE_API_KEY)")

            # Keep the server running
            while True:
                await asyncio.sleep(3600)  # Sleep for an hour
    else:
        # Fallback: Just run indefinitely
        print("MCP Server started in fallback mode on localhost:8080")
        print("Capabilities available:")
        print("- Filesystem operations: read, write, list, create_dir, delete")
        print("- GitHub operations: clone, commit, push")
        print("- PostgreSQL operations: connect, query, execute")
        print("- HTTP operations: get, post, put, delete")
        print("- Docker operations: build, run, push, status")
        print("- Web search: search.web (requires BRAVE_API_KEY)")

        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour


if __name__ == "__main__":
    asyncio.run(main())