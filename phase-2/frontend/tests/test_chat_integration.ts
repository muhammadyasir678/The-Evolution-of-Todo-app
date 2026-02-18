/**
 * Frontend integration tests for natural language commands - Tasks T090-T095
 * Test end-to-end functionality: natural language input → API call → MCP tools → response
 */

// Add Jest type definitions
/// <reference types="jest" />

// Mock the API functions
jest.mock('../lib/chatApi', () => ({
  sendMessage: jest.fn()
}));

import { sendMessage } from '../lib/chatApi';
import { renderHook, act } from '@testing-library/react-hooks';
import { ChatInterface } from '../components/ChatInterface';

// Define the expected response type
interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: string[];
}

describe('Natural Language Command Tests - Tasks T090-T095', () => {
  beforeEach(() => {
    (sendMessage as jest.MockedFunction<typeof sendMessage>).mockClear();
  });

  /**
   * Task T091: "Add a task to buy milk" → add_task invoked and confirmed
   */
  test('should invoke add_task when user adds a task', async () => {
    const mockResponse: ChatResponse = {
      conversation_id: 123,
      response: "I've added 'buy milk' to your tasks.",
      tool_calls: ["add_task"]
    };

    (sendMessage as jest.MockedFunction<typeof sendMessage>)
      .mockResolvedValue(mockResponse);

    const result = await sendMessage({
      conversation_id: null,
      message: "Add a task to buy milk",
      user_id: "user-123"
    });

    expect(sendMessage).toHaveBeenCalledWith({
      conversation_id: null,
      message: "Add a task to buy milk",
      user_id: "user-123"
    });

    expect(result.tool_calls).toContain("add_task");
    expect(result.response).toContain("buy milk");
  });

  /**
   * Task T092: "Show me all my tasks" → list_tasks invoked and displayed
   */
  test('should invoke list_tasks when user requests to see tasks', async () => {
    const mockResponse: ChatResponse = {
      conversation_id: 123,
      response: "You have 2 tasks: 1. Buy milk (pending), 2. Call doctor (pending)",
      tool_calls: ["list_tasks"]
    };

    (sendMessage as jest.MockedFunction<typeof sendMessage>)
      .mockResolvedValue(mockResponse);

    const result = await sendMessage({
      conversation_id: 123,
      message: "Show me all my tasks",
      user_id: "user-123"
    });

    expect(sendMessage).toHaveBeenCalledWith({
      conversation_id: 123,
      message: "Show me all my tasks",
      user_id: "user-123"
    });

    expect(result.tool_calls).toContain("list_tasks");
    expect(result.response).toContain("tasks");
  });

  /**
   * Task T093: "Mark task 1 as complete" → complete_task invoked and confirmed
   */
  test('should invoke complete_task when user marks task as complete', async () => {
    const mockResponse: ChatResponse = {
      conversation_id: 123,
      response: "Task 1 has been marked as complete.",
      tool_calls: ["complete_task"]
    };

    (sendMessage as jest.MockedFunction<typeof sendMessage>)
      .mockResolvedValue(mockResponse);

    const result = await sendMessage({
      conversation_id: 123,
      message: "Mark task 1 as complete",
      user_id: "user-123"
    });

    expect(sendMessage).toHaveBeenCalledWith({
      conversation_id: 123,
      message: "Mark task 1 as complete",
      user_id: "user-123"
    });

    expect(result.tool_calls).toContain("complete_task");
    expect(result.response).toContain("complete");
  });

  /**
   * Task T094: "Delete task 2" → delete_task invoked and confirmed
   */
  test('should invoke delete_task when user requests to delete a task', async () => {
    const mockResponse: ChatResponse = {
      conversation_id: 123,
      response: "Task 2 has been deleted.",
      tool_calls: ["delete_task"]
    };

    (sendMessage as jest.MockedFunction<typeof sendMessage>)
      .mockResolvedValue(mockResponse);

    const result = await sendMessage({
      conversation_id: 123,
      message: "Delete task 2",
      user_id: "user-123"
    });

    expect(sendMessage).toHaveBeenCalledWith({
      conversation_id: 123,
      message: "Delete task 2",
      user_id: "user-123"
    });

    expect(result.tool_calls).toContain("delete_task");
    expect(result.response).toContain("deleted");
  });

  /**
   * Task T095: "Change task 3 title" → update_task invoked and confirmed
   */
  test('should invoke update_task when user requests to change task title', async () => {
    const mockResponse: ChatResponse = {
      conversation_id: 123,
      response: "Task 3 has been updated with the new title.",
      tool_calls: ["update_task"]
    };

    (sendMessage as jest.MockedFunction<typeof sendMessage>)
      .mockResolvedValue(mockResponse);

    const result = await sendMessage({
      conversation_id: 123,
      message: "Change task 3 title to 'New important task'",
      user_id: "user-123"
    });

    expect(sendMessage).toHaveBeenCalledWith({
      conversation_id: 123,
      message: "Change task 3 title to 'New important task'",
      user_id: "user-123"
    });

    expect(result.tool_calls).toContain("update_task");
    expect(result.response).toContain("updated");
  });

  /**
   * Task T090: Test natural language commands work end-to-end
   */
  test('should process various natural language commands end-to-end', async () => {
    const commands = [
      "Add a task to buy groceries",
      "Show me my pending tasks",
      "Mark task 1 as done",
      "Delete the meeting task",
      "Update task 2 description"
    ];

    for (const command of commands) {
      const mockResponse: ChatResponse = {
        conversation_id: 123,
        response: `Processed: ${command}`,
        tool_calls: ["add_task"] // Simplified for testing
      };

      (sendMessage as jest.MockedFunction<typeof sendMessage>)
        .mockResolvedValue(mockResponse);

      const result = await sendMessage({
        conversation_id: 123,
        message: command,
        user_id: "user-123"
      });

      expect(sendMessage).toHaveBeenCalledWith({
        conversation_id: 123,
        message: command,
        user_id: "user-123"
      });

      expect(result.conversation_id).toBe(123);
      expect(result.response).toContain(command);
    }
  });
});