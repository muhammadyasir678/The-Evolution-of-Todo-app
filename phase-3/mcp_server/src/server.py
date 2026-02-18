"""
MCP Server Entry Point - Task T016
Initialize MCP Server with name "todo-mcp-server" and register all 5 tools
"""
import asyncio
from mcp.server import Server
from mcp.types import TextContent, PromptMessage, ListPromptsResult, GetPromptResult, Prompt
from pydantic import BaseModel
from typing import List
import json
from .tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    DeleteTaskRequest, UpdateTaskRequest
)

# Initialize MCP Server with name "todo-mcp-server"
server = Server("todo-mcp-server")

@server.list_prompts()
async def handle_list_prompts(request) -> ListPromptsResult:
    return ListPromptsResult(prompts=[])

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
    """Handle get prompt request."""
    return GetPromptResult(
        prompt=Prompt(
            name=name,
            description="Todo prompt",
            messages=[PromptMessage(content=TextContent(type="text", text="Default prompt"))]
        )
    )


# Register all 5 MCP tools as specified in task T025
@server.call_tool("add_task")
async def handle_add_task(params: AddTaskRequest) -> dict:
    """Handle add_task tool calls."""
    return await add_task(params)

@server.call_tool("list_tasks")
async def handle_list_tasks(params: ListTasksRequest) -> dict:
    """Handle list_tasks tool calls."""
    return await list_tasks(params)

@server.call_tool("complete_task")
async def handle_complete_task(params: CompleteTaskRequest) -> dict:
    """Handle complete_task tool calls."""
    return await complete_task(params)

@server.call_tool("delete_task")
async def handle_delete_task(params: DeleteTaskRequest) -> dict:
    """Handle delete_task tool calls."""
    return await delete_task(params)

@server.call_tool("update_task")
async def handle_update_task(params: UpdateTaskRequest) -> dict:
    """Handle update_task tool calls."""
    return await update_task(params)


async def main():
    """Main entry point for the MCP server with stdio transport."""
    async with server.serve_stdio():
        print("MCP Server started and listening on stdio...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())