---
id: 4
title: "Create Task Breakdown for Phase I"
stage: tasks
feature: "console-todo"
date_iso: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
branch: 001-console-todo
user: user
command: "/sp.tasks"
labels: ["tasks", "phase1", "console-app", "breakdown"]

link_spec: "specs/001-console-todo/spec.md"
link_plan: "specs/001-console-todo/plan.md"
link_tasks: "specs/001-console-todo/tasks.md"
link_ticket: null
link_adr: null
link_pr: null

files_yaml:
  - "specs/001-console-todo/tasks.md"
  - "history/prompts/001-console-todo/4-create-task-breakdown-for-phase-i.tasks.prompt.md"

tests_yaml:
  - "No tests needed for task creation"

prompt_text: |

  PHASE: Phase I - In-Memory Python Console App

  BASE: Approved speckit.plan for Phase I

  TASKS:

  T-001: Create Project Structure
  - Create phase-1/ directory
  - Create src/ subdirectory with __init__.py
  - Create tests/ subdirectory with __init__.py
  - Create pyproject.toml for UV
  - Create README.md with placeholder content
  - Verify structure matches plan

  T-002: Implement Task Model
  - Create src/models.py
  - Define Task dataclass with fields: id, title, description, completed, created_at
  - Add __str__ method for readable output
  - Add validation in __post_init__ for title length (1-200 chars)
  - Add validation for description length (max 1000 chars)
  - Reference: speckit.plan §Data Model

  T-003: Implement TaskManager Class
  - Create src/task_manager.py
  - Initialize tasks dict and next_id counter
  - Implement add_task(title, description) → Task
  - Implement get_all_tasks() → list[Task]
  - Implement get_task(task_id) → Task | None
  - Implement update_task(task_id, title, description) → bool
  - Implement delete_task(task_id) → bool
  - Implement toggle_complete(task_id) → bool
  - Reference: speckit.plan §Technical Approach

  T-004: Implement Input Validation Utilities
  - Create src/utils.py
  - Implement validate_title(title) → bool, error_message
  - Implement validate_description(description) → bool, error_message
  - Implement validate_task_id(task_id_str) → int | None
  - Implement validate_menu_choice(choice_str) → int | None
  - Reference: speckit.plan §Validation Rules

  T-005: Implement UI Display Functions
  - Create src/ui.py
  - Implement display_menu() - show menu options
  - Implement display_tasks(tasks) - formatted task list
  - Implement display_task(task) - single task details
  - Implement display_error(message) - error formatting
  - Implement display_success(message) - success formatting
  - Use status symbols: ✓ for complete, ○ for incomplete
  - Reference: speckit.plan §Operation Flows

  T-006: Implement UI Input Functions
  - In src/ui.py
  - Implement get_menu_choice() → int
  - Implement get_task_input() → tuple[str, str] (title, description)
  - Implement get_task_id() → int
  - Implement get_confirmation() → bool
  - Handle invalid input with error messages
  - Reference: speckit.plan §Operation Flows

  T-007: Implement Main Application Loop
  - Create src/main.py
  - Initialize TaskManager instance
  - Implement main menu loop
  - Route menu choices to appropriate handlers
  - Implement add_task_flow()
  - Implement view_tasks_flow()
  - Implement update_task_flow()
  - Implement delete_task_flow()
  - Implement toggle_complete_flow()
  - Handle exit gracefully
  - Reference: speckit.plan §CLI Menu System

  T-008: Add Error Handling
  - In src/main.py
  - Wrap main loop in try-except for KeyboardInterrupt
  - Add graceful exit message
  - Handle all TaskManager exceptions
  - Display user-friendly error messages
  - Reference: speckit.plan §Error Handling

  T-009: Write Unit Tests
  - Create tests/test_models.py - test Task validation
  - Create tests/test_task_manager.py - test all CRUD operations
  - Test edge cases: empty list, invalid IDs, duplicate operations
  - Verify error handling
  - Reference: speckit.plan §Testing Strategy

  T-010: Create Documentation
  - Update README.md with:
    - Project description
    - Setup instructions (UV installation)
    - How to run: `uv run python src/main.py`
    - Feature list (5 operations)
    - WSL 2 setup for Windows users
  - Reference: speckit.specify §Acceptance Criteria

  T-011: Manual Testing and Validation
  - Test all 5 operations end-to-end
  - Test input validation (invalid inputs)
  - Test error scenarios (non-existent IDs)
  - Test edge cases (empty list, special characters)
  - Verify all acceptance criteria met
  - Reference: speckit.specify §Acceptance Criteria

response_text: |
  Successfully created a comprehensive task breakdown for Phase I - In-Memory Python Console App with 39 specific tasks organized across 8 phases:

  1. **Phase 1: Project Setup** (Tasks T001-T006) - Creating the foundational project structure
  2. **Phase 2: Foundational Components** (Tasks T007-T010) - Core models and utilities
  3. **Phase 3: User Story 1** (Tasks T011-T017) - Add and view tasks functionality (P1 priority)
  4. **Phase 4: User Story 2** (Tasks T018-T022) - Update and complete tasks (P2 priority)
  5. **Phase 5: User Story 3** (Tasks T023-T025) - Delete tasks (P3 priority)
  6. **Phase 6: Error Handling and Validation** (Tasks T026-T030) - Robust error handling
  7. **Phase 7: Testing** (Tasks T031-T034) - Unit tests for all components
  8. **Phase 8: Documentation and Polish** (Tasks T035-T039) - Documentation and final validation

  The tasks follow the required checklist format with proper IDs, story labels, and parallelization markers. The breakdown maintains the user-story-centric organization with independent test criteria for each story. The MVP scope focuses on completing User Story 1 first, which provides core functionality.

outcome: |
  Created a detailed task breakdown with 39 specific, actionable tasks organized by user story priority, enabling independent implementation and testing of each feature.

evaluation: |
  The task breakdown comprehensively covers all requirements from the original request with proper organization by user stories, clear dependencies, and parallel execution opportunities identified. Each task is specific enough to be executed independently while maintaining the overall project coherence.
---
