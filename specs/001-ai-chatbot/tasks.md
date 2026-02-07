# Implementation Tasks: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot | **Branch**: `001-ai-chatbot` | **Date**: [DATE]
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

## Dependencies

- Phase II: Full Stack Todo App with Authentication must be complete
- Neon Serverless PostgreSQL configured and accessible
- OpenAI API key available

## Implementation Strategy

- **MVP Approach**: Begin with User Story 1 (Natural Language Task Management) to deliver core functionality early
- **Incremental Delivery**: Build foundational components first, then add advanced features
- **Parallel Work Streams**: Backend and MCP server can be developed in parallel, frontend can be built once API is stable
- **Stateless Architecture**: Maintain no in-memory conversation state in servers

## User Story Completion Order

1. **US1 - Natural Language Task Management** (P1) - Foundation
2. **US2 - Task Operations via Chat** (P1) - Enhancement
3. **US3 - Persistent Conversation Context** (P2) - Advanced feature

## Parallel Execution Examples

- **Team A**: MCP Server development (T201-T204)
- **Team B**: Backend API development (T205-T208)
- **Team C**: Frontend Chat Interface (T209-T213)
- **Team D**: Testing and documentation (T215-T220)

---

## Phase 1: Project Setup

### Setup Tasks
- [x] T001 Create phase-3 directory structure with backend/, frontend/, and mcp-server/ subdirectories
- [x] T002 Configure development environment with Python 3.13+, Node.js 18+, and uv package manager
- [x] T003 Initialize backend as FastAPI project with proper dependencies
- [x] T004 Initialize frontend as Next.js 16+ project with TypeScript and Tailwind CSS
- [x] T005 Set up MCP server project with Official MCP SDK dependency

## Phase 2: Foundational Infrastructure

### Database Extensions
- [x] T010 [P] Extend database models in backend/app/models.py to add Conversation model with fields: id, user_id, created_at, updated_at
- [x] T011 [P] Extend database models in backend/app/models.py to add Message model with fields: id, user_id, conversation_id, role, content, created_at
- [x] T012 [P] Add database indexes on user_id and conversation_id for Conversation and Message models
- [x] T013 Create database migration script for Conversation and Message tables

### MCP Server Foundation
- [x] T015 [P] Create MCP server project structure in phase-3/mcp-server/ with proper pyproject.toml configuration
- [x] T016 [P] Set up MCP server entry point in mcp-server/src/server.py with name "todo-mcp-server"
- [x] T017 [P] Configure stdio server transport for MCP server

## Phase 3: User Story 1 - Natural Language Task Management (P1)

### MCP Tools Implementation
- [x] T020 [P] [US1] Implement add_task MCP tool in mcp-server/src/tools.py with parameters: user_id, title, description
- [x] T021 [P] [US1] Implement list_tasks MCP tool in mcp-server/src/tools.py with parameters: user_id, status
- [x] T022 [P] [US1] Implement complete_task MCP tool in mcp-server/src/tools.py with parameters: user_id, task_id
- [x] T023 [P] [US1] Implement delete_task MCP tool in mcp-server/src/tools.py with parameters: user_id, task_id
- [x] T024 [P] [US1] Implement update_task MCP tool in mcp-server/src/tools.py with parameters: user_id, task_id, title, description
- [x] T025 [US1] Register all 5 MCP tools with the MCP server in mcp-server/src/server.py

### Backend Agent Configuration
- [x] T030 [US1] Install OpenAI Agents SDK in backend and add OPENAI_API_KEY to environment
- [x] T031 [US1] Create agent configuration in backend/app/agent.py with name "Todo Assistant" and model gpt-4o
- [x] T032 [US1] Write agent instructions for task management in backend/app/agent.py
- [x] T033 [US1] Register MCP tools with the OpenAI agent

### Chat API Endpoint
- [x] T035 [US1] Create chat routes module in backend/app/routes/chat.py
- [x] T036 [US1] Implement POST /api/{user_id}/chat endpoint that accepts conversation_id (optional) and message (required)
- [x] T037 [US1] Add JWT authentication to chat endpoint using get_current_user
- [x] T038 [US1] Implement logic to create new Conversation if conversation_id is null
- [x] T039 [US1] Implement logic to fetch conversation history from messages table

### Basic Frontend Components
- [x] T040 [P] [US1] Install OpenAI ChatKit in frontend with NEXT_PUBLIC_OPENAI_DOMAIN_KEY in environment
- [x] T041 [P] [US1] Create ChatMessage component in frontend/components/ChatMessage.tsx to display message bubbles with role differentiation
- [x] T042 [P] [US1] Create basic ChatInterface component in frontend/components/ChatInterface.tsx with input field and send button
- [x] T043 [US1] Create chat page in frontend/app/protected/chat/page.tsx with protected route

## Phase 4: User Story 2 - Task Operations via Chat (P1)

### Enhanced Chat Processing
- [x] T050 [US2] Enhance chat endpoint to build message array combining history and new message
- [x] T051 [US2] Enhance chat endpoint to call agent with messages and process responses
- [x] T052 [US2] Enhance chat endpoint to store user message in database
- [x] T053 [US2] Enhance chat endpoint to store assistant response in database
- [x] T054 [US2] Enhance chat endpoint to return conversation_id, response, and tool_calls

### MCP Tool Enhancements
- [x] T055 [P] [US2] Add proper error handling to all MCP tools with structured responses
- [x] T056 [P] [US2] Implement user isolation in all MCP tools (user A cannot access user B's tasks)
- [x] T057 [US2] Enhance list_tasks tool to properly filter by status (completed/incomplete)

### Frontend Chat Features
- [x] T060 [US2] Enhance ChatInterface component to integrate with OpenAI ChatKit components
- [x] T061 [US2] Enhance ChatInterface to display loading/typing indicator while waiting for AI
- [x] T062 [US2] Enhance ChatInterface to handle conversation_id state
- [x] T063 [US2] Create chat API client in frontend/lib/chatApi.ts for sending messages
- [x] T064 [US2] Enhance ChatInterface to scroll to bottom on new messages

## Phase 5: User Story 3 - Persistent Conversation Context (P2)

### State Management
- [x] T070 [US3] Ensure conversation history is properly loaded from database and passed to agent
- [x] T071 [US3] Implement conversation resume functionality after server restart
- [x] T072 [US3] Add proper timestamp formatting to ChatMessage component
- [x] T073 [US3] Enhance message storage to maintain chronological order with proper indexing

### Enhanced User Experience
- [x] T075 [US3] Add error handling for API client in frontend/lib/chatApi.ts
- [x] T076 [US3] Add proper styling for different message roles (user vs assistant) in ChatMessage component
- [x] T077 [US3] Implement message history scrolling in ChatInterface component
- [x] T078 [US3] Add user authentication integration to chat interface

## Phase 6: Integration and Testing

### Backend Testing
- [x] T080 [P] [US1] Create tests for MCP tools in mcp-server/tests/test_tools.py
- [x] T081 [P] [US2] Create tests for chat endpoint in backend/tests/test_chat.py
- [x] T082 [US3] Create integration tests for end-to-end flow: user message → agent → MCP tools → database → response

### MCP Server Testing
- [x] T085 [P] [US1] Test add_task creates task in database with proper user isolation
- [x] T086 [P] [US1] Test list_tasks returns user-specific tasks with status filtering
- [x] T087 [P] [US2] Test complete_task toggles status and respects user isolation
- [x] T088 [P] [US2] Test delete_task removes task and respects user isolation
- [x] T089 [P] [US2] Test update_task modifies task and respects user isolation

### Frontend Testing
- [x] T090 [US3] Test natural language commands work end-to-end:
- [x] T091 [US3] "Add a task to buy milk" → add_task invoked and confirmed
- [x] T092 [US3] "Show me all my tasks" → list_tasks invoked and displayed
- [x] T093 [US3] "Mark task 1 as complete" → complete_task invoked and confirmed
- [x] T094 [US3] "Delete task 2" → delete_task invoked and confirmed
- [x] T095 [US3] "Change task 3 title" → update_task invoked and confirmed

## Phase 7: Polish & Cross-Cutting Concerns

### Production Preparation
- [x] T100 Configure OpenAI domain allowlist for production deployment
- [x] T101 Update documentation in phase-3/README.md with MCP server setup instructions
- [x] T102 Update documentation with OpenAI API key configuration instructions
- [x] T103 Update documentation with OpenAI ChatKit domain allowlist setup
- [x] T104 Add natural language command examples to documentation
- [x] T105 Deploy MCP server with proper DATABASE_URL configuration

### Quality Assurance
- [x] T110 Verify conversation persistence across server restarts
- [x] T111 Verify user isolation in production environment
- [x] T112 Test multiple users with independent conversations
- [x] T113 Verify stateless architecture (restart server, resume conversation)
- [x] T114 Add CLAUDE.md with Phase III implementation notes
- [x] T115 Create comprehensive testing of all natural language commands in production

### Documentation
- [x] T120 Complete API documentation for chat endpoint
- [x] T121 Document MCP tool specifications and parameters
- [x] T122 Create user guide for natural language commands
- [x] T123 Update overall project README with Phase III features