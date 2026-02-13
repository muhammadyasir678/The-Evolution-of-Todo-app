"""
Entry point for the MCP server.
This file is used by the Dockerfile to start the application.
"""
from src.server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())