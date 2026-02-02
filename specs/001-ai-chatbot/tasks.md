# Tasks: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-chatbot
**Generated from**: specs/001-ai-chatbot/spec.md and specs/001-ai-chatbot/plan.md

## Implementation Strategy

Build an AI-powered todo chatbot with natural language interface using OpenAI ChatKit frontend, FastAPI backend with OpenAI Agents SDK, and MCP server with 5 stateless tools. Implement in priority order: User Story 1 (core functionality), User Story 2 (full operations), User Story 3 (persistence).

**MVP Scope**: User Story 1 only - basic natural language task management with chat interface.

## Phase 1: Setup

### Goal
Initialize project structure and install dependencies.

### Tasks
- [ ] T001 Create phase-3/ directory structure with frontend/, backend/, and mcp-server/ subdirectories
- [ ] T002 Setup backend project with FastAPI, SQLModel, and existing dependencies
- [ ] T003 Setup frontend project with Next.js 16+, TypeScript, and Tailwind CSS
- [ ] T004 Install OpenAI Agents SDK in backend: uv add openai-agents-sdk
- [ ] T005 [P] Install MCP SDK in mcp-server: uv init && uv add mcp
- [ ] T006 [P] Install OpenAI ChatKit in frontend: npm install @openai/chatkit

## Phase 2: Foundational Components

### Goal
Implement database models and MCP server foundation that all user stories depend on.

### Tasks
- [ ] T010 Extend backend/app/models.py with Conversation model: id, user_id, created_at, updated_at
- [ ] T011 Extend backend/app/models.py with Message model: id, user_id, conversation_id, role, content, created_at
- [ ] T012 Add indexes on user_id and conversation_id for performance
- [ ] T013 Create database migration script for Conversation and Message models
- [ ] T014 Create mcp-server/src/init.py
- [ ] T015 Create mcp-server/src/server.py with MCP server initialization
- [ ] T016 Create mcp-server/src/tools.py with database connection utilities

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

### Goal
Enable users to manage todo tasks through a conversational interface using natural language commands.

### Independent Test Criteria
Can be fully tested by typing natural language commands into the chat interface and verifying the AI correctly interprets intent and performs the requested task operations, delivering immediate value of conversational task management.

### Tasks
- [ ] T020 [US1] Implement add_task MCP tool with parameters: user_id, title, description
- [ ] T021 [US1] Implement list_tasks MCP tool with parameters: user_id, status
- [ ] T022 [US1] Create backend/app/agent.py with OpenAI Agent configuration
- [ ] T023 [US1] Configure agent instructions for task management and register MCP tools
- [ ] T024 [US1] Implement POST /api/{user_id}/chat endpoint in backend/app/routes/chat.py
- [ ] T025 [US1] Add JWT authentication to chat endpoint using get_current_user
- [ ] T026 [US1] Implement conversation history fetching and message persistence
- [ ] T027 [US1] Create frontend/components/ChatMessage.tsx for message display
- [ ] T028 [US1] Create frontend/lib/chatApi.ts with sendMessage function
- [ ] T029 [US1] Create frontend/components/ChatInterface.tsx with ChatKit integration
- [ ] T030 [US1] Create frontend/app/(protected)/chat/page.tsx with ChatInterface component

## Phase 4: User Story 2 - Task Operations via Chat (Priority: P1)

### Goal
Allow users to perform all five basic todo operations (add, list, complete, delete, update) through natural language commands.

### Independent Test Criteria
Can be tested by issuing various task operation commands through the chat interface and verifying each operation (complete, delete, update) executes correctly and the AI confirms the action.

### Tasks
- [ ] T040 [US2] Implement complete_task MCP tool with parameters: user_id, task_id
- [ ] T041 [US2] Implement delete_task MCP tool with parameters: user_id, task_id
- [ ] T042 [US2] Implement update_task MCP tool with parameters: user_id, task_id, title, description
- [ ] T043 [US2] Update agent.py to handle all 5 MCP tools properly
- [ ] T044 [US2] Update chat endpoint to support all task operations
- [ ] T045 [US2] Enhance ChatInterface to handle all operation confirmations

## Phase 5: User Story 3 - Persistent Conversation Context (Priority: P2)

### Goal
Enable users to continue conversations with the AI after closing and reopening the browser or after server restarts.

### Independent Test Criteria
Can be tested by starting a conversation, performing several task operations, closing the browser, restarting the server, reopening the chat, and verifying that conversation history is restored and the AI maintains context.

### Tasks
- [ ] T050 [US3] Enhance conversation handling to resume existing conversations
- [ ] T051 [US3] Implement conversation history loading in frontend ChatInterface
- [ ] T052 [US3] Add conversation_id tracking in frontend component state
- [ ] T053 [US3] Update agent to include conversation context in responses
- [ ] T054 [US3] Test conversation persistence after server restart

## Phase 6: Testing & Validation

### Goal
Validate all functionality works as expected with proper test coverage.

### Tasks
- [ ] T060 Create mcp-server/tests/test_tools.py with unit tests for all 5 tools
- [ ] T061 Create backend/tests/test_chat.py with tests for chat endpoint
- [ ] T062 Implement end-to-end integration tests for natural language commands
- [ ] T063 Test user isolation (user A cannot access user B's data)
- [ ] T064 Test all acceptance scenarios from user stories
- [ ] T065 Performance testing to ensure <3s response time for 95% of requests

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation, error handling, and production readiness.

### Tasks
- [ ] T070 Add proper error handling to MCP tools with structured responses
- [ ] T071 Add error boundaries and user feedback in frontend components
- [ ] T072 Update phase-3/README.md with setup and deployment instructions
- [ ] T073 Configure OpenAI domain allowlist for production deployment
- [ ] T074 Add logging and monitoring capabilities
- [ ] T075 Security review: validate user isolation and JWT authentication
- [ ] T076 Update CLAUDE.md with Phase III implementation notes
- [ ] T077 Deploy MCP server and verify production connectivity
- [ ] T078 Final end-to-end testing in production-like environment

## Dependencies

- **User Story 2** depends on foundational MCP tools from **Phase 2**
- **User Story 3** depends on conversation persistence from **Phase 2**
- **Phase 6** (Testing) can run in parallel with all user stories once implementation is complete
- **Phase 7** (Polish) should run after all functionality is implemented and tested

## Parallel Execution Opportunities

- MCP tools implementation can be parallelized (T020, T021 for US1; T040, T041, T042 for US2)
- Frontend components can be developed in parallel with backend APIs (T027-T030)
- Testing can be done in parallel with implementation for each user story