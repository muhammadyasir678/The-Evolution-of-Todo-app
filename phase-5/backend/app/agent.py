"""
AI Agent Configuration - Tasks T031, T032, T033
Configure OpenAI Agent with name "Todo Assistant" and register MCP tools
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any, cast
from .models import Task

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_todo_assistant():
    """
    Create and return the Todo Assistant agent with name "Todo Assistant"
    and model gpt-4o as specified in task T031
    """
    # Create assistant with instructions for task management
    assistant = client.beta.assistants.create(
        name="Todo Assistant",
        instructions=get_agent_instructions(),  # Task T032: Write agent instructions for task management
        model="gpt-4o",  # Set model to gpt-4o as required
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks from the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "status": {"type": "string", "enum": ["all", "completed", "pending"], "description": "Filter tasks by status"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task"},
                            "description": {"type": "string", "description": "New description for the task"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]
    )

    return assistant

def get_agent_instructions() -> str:
    """
    Task T032: Write agent instructions for task management
    These instructions guide the natural language understanding for the todo assistant
    """
    instructions = """
    You are a helpful Todo Assistant that helps users manage their tasks through natural language conversations.
    Your purpose is to interpret user requests and use the provided tools to manage tasks in their todo list.

    When users speak in natural language:
    - "Add a task to buy milk" → call add_task with title "buy milk"
    - "Show me my tasks" → call list_tasks to show all tasks
    - "What's pending?" → call list_tasks with status "pending" to show incomplete tasks
    - "Mark task 1 as complete" → call complete_task with task_id 1
    - "Delete the meeting task" → call delete_task after identifying the task
    - "Change task 1 to 'Call mom tonight'" → call update_task with new title

    Always confirm actions taken and respond in a friendly, conversational manner.
    If a user requests multiple actions, perform them one by one and acknowledge each.
    Only operate on tasks that belong to the user (respect user_id for data isolation).
    """
    return instructions

def run_agent(messages: List[Dict[str, Any]], user_id: str) -> Dict[str, Any]:
    """
    Task T033: Create run_agent function that accepts messages and returns response
    This function processes messages through the OpenAI agent with registered MCP tools
    """
    # Create a thread for this conversation
    thread = client.beta.threads.create(
        messages=cast(Any, messages)
    )

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=get_todo_assistant().id,
        # Pass the user_id to be used by tools for isolation
        additional_instructions=f"The current user ID is {user_id}. Ensure all operations are scoped to this user only."
    )

    # Poll for completion
    import time
    while run.status in ['queued', 'in_progress']:
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Get the messages from the thread
    messages_response = client.beta.threads.messages.list(thread_id=thread.id)

    # Format the response
    response_messages = []
    for msg in messages_response.data:
        if msg.role == "assistant":
            content = ""
            for item in msg.content:
                if item.type == "text":
                    content += item.text.value
            response_messages.append({
                "role": msg.role,
                "content": content
            })

    # Get any tool calls that were made
    tool_calls: list[str] = []

    if run.status == "requires_action" and run.required_action:
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
           if tool_call.function:
               tool_calls.append(tool_call.function.name)
    return {
        "response": response_messages[-1]["content"] if response_messages else "I processed your request.",
        "tool_calls": tool_calls,
        "thread_id": thread.id
    }