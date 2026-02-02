---
name: ai-agent-dev
description: Build production-ready AI agents, conversational interfaces, and MCP servers using OpenAI SDKs and modern agent patterns.
---

# AI Agent Development

## Instructions

1. **Conversational Interfaces**
   - Build chat-based UIs using OpenAI ChatKit
   - Support multi-turn conversations
   - Handle user intent, context, and follow-ups

2. **Agent Logic**
   - Implement AI behavior using OpenAI Agents SDK
   - Design agent roles, goals, and constraints
   - Manage reasoning, tool usage, and responses

3. **MCP Server Development**
   - Create MCP servers using the Official MCP SDK
   - Expose tools, resources, and prompts via MCP
   - Follow Model Context Protocol specifications

4. **State Management**
   - Design stateless chat endpoints
   - Persist conversation state in databases
   - Rehydrate context on each request

5. **Tooling & Function Calling**
   - Design reusable agent tools
   - Implement function calling patterns
   - Validate inputs and outputs strictly

6. **Natural Language Processing**
   - Interpret natural language commands
   - Map user intent to agent actions
   - Handle ambiguities and edge cases

7. **Conversation Management**
   - Track conversation history and metadata
   - Implement memory strategies (short-term vs long-term)
   - Handle session lifecycle and resets

## Best Practices

- Keep agents focused on a single responsibility
- Prefer stateless APIs with explicit state persistence
- Validate all tool inputs and outputs
- Design tools as composable, testable units
- Log agent decisions and tool calls for debugging
- Follow clean architecture: UI → Agent → Tools → Data
- Secure MCP servers and agent endpoints

## Example Structure

```ts
// Agent definition
const agent = new Agent({
  name: "SupportAgent",
  instructions: "Help users by answering questions and calling tools when needed",
  tools: [searchTool, databaseTool],
});

// Stateless chat endpoint
export async function chatHandler(request) {
  const state = await loadConversationState(request.sessionId);

  const response = await agent.run({
    messages: state.messages,
    input: request.userMessage,
  });

  await saveConversationState(request.sessionId, response.messages);

  return response.output;
}
