# Tasks: Phase I - In-Memory Python Console App

**Feature**: Phase I - In-Memory Python Console App
**Branch**: 001-console-todo
**Based on**: Implementation Plan and Specification

## Implementation Strategy

This implementation follows the spec-driven approach with user stories as the organizing principle. Each user story is developed as an independently testable increment, starting with the core functionality (US1) and building up to full CRUD operations.

**MVP Scope**: Complete User Story 1 (Add and View Tasks) first, which provides a minimally viable console todo application.

## Phase 1: Project Setup

Initialize the project structure and foundational components.

- [X] T001 Create phase-1/ directory
- [X] T002 Create src/ subdirectory with __init__.py
- [X] T003 Create tests/ subdirectory with __init__.py
- [X] T004 Create pyproject.toml for UV package management
- [X] T005 Create README.md with placeholder content
- [X] T006 Verify structure matches implementation plan

## Phase 2: Foundational Components

Core components that support all user stories.

- [X] T007 [P] Implement Task model in src/models.py with id, title, description, completed, created_at
- [X] T008 [P] Implement Task validation in src/models.py for title (1-200 chars) and description (max 1000 chars)
- [X] T009 [P] Implement input validation utilities in src/utils.py for title, description, task_id, and menu_choice
- [X] T010 [P] Implement TaskManager class in src/task_manager.py with tasks dict and next_id counter

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

As a user, I want to add new todo tasks and view my existing tasks so that I can keep track of my work. I can launch the console application, select the option to add a task, enter a title and optional description, and then view a list of all my tasks with their status indicators.

**Goal**: Core functionality for creating and viewing tasks with status indicators.

**Independent Test**: Can be fully tested by launching the app, adding a few tasks, and viewing the task list to verify that tasks are properly stored and displayed with correct status indicators.

**Acceptance Scenarios**:
1. Given the console app is running, When user selects "Add Task" option, enters a title and optional description, Then a new task is created with a unique ID and status of incomplete, and confirmation is shown to the user
2. Given the console app has multiple tasks, When user selects "View Task List" option, Then all tasks are displayed with ID, title, status indicator (✓ for complete, ○ for incomplete), and description

- [X] T011 [P] [US1] Implement add_task method in TaskManager with unique ID generation and default incomplete status
- [X] T012 [P] [US1] Implement get_all_tasks method in TaskManager to return all tasks
- [X] T013 [P] [US1] Implement UI display functions in src/ui.py for menu and task listings with status symbols ✓/○
- [X] T014 [P] [US1] Implement UI input functions in src/ui.py for getting task title and description
- [X] T015 [US1] Implement main application loop in src/main.py with add task and view task options
- [X] T016 [US1] Implement add_task_flow in main.py to handle the complete add task workflow
- [X] T017 [US1] Implement view_tasks_flow in main.py to handle the complete view task workflow

## Phase 4: User Story 2 - Update and Complete Tasks (Priority: P2)

As a user, I want to update my task details and mark tasks as complete so that I can keep my todo list accurate and track my progress. I can select a task by ID, modify its title or description, or toggle its completion status.

**Goal**: Enhance functionality by allowing users to maintain and track their tasks.

**Independent Test**: Can be fully tested by creating tasks, updating their details, and marking them as complete/incomplete to verify that changes are properly reflected.

**Acceptance Scenarios**:
1. Given the console app has existing tasks, When user selects "Update Task" and provides a valid task ID with new details, Then the task is updated with the new information and confirmation is shown
2. Given a task exists with incomplete status, When user selects "Mark as Complete" for that task, Then the task's status changes to complete and visual confirmation is shown

- [X] T018 [P] [US2] Implement update_task method in TaskManager to modify title and/or description by ID
- [X] T019 [P] [US2] Implement toggle_task_completion method in TaskManager to flip completion status
- [X] T020 [P] [US2] Implement UI input functions in src/ui.py for getting task ID and update details
- [X] T021 [US2] Implement update_task_flow in main.py to handle the complete update task workflow
- [X] T022 [US2] Implement toggle_complete_flow in main.py to handle the complete/incomplete toggle workflow

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

As a user, I want to remove tasks that are no longer needed so that I can keep my todo list organized and focused on relevant items. I can select a task by ID and confirm deletion to remove it permanently.

**Goal**: Complete the CRUD operations for tasks, giving users full control over their todo list management.

**Independent Test**: Can be fully tested by creating tasks, deleting them, and verifying that they no longer appear in the task list.

**Acceptance Scenarios**:
1. Given the console app has existing tasks, When user selects "Delete Task" and provides a valid task ID, Then the system asks for confirmation before removing the task
2. Given user confirms deletion, When deletion process completes, Then the task is removed from the list and confirmation message is displayed

- [X] T023 [P] [US3] Implement delete_task method in TaskManager with confirmation requirement
- [X] T024 [P] [US3] Implement UI input functions in src/ui.py for getting task ID and confirmation
- [X] T025 [US3] Implement delete_task_flow in main.py to handle the complete delete task workflow with confirmation

## Phase 6: Error Handling and Validation

Robust error handling and validation across all operations.

- [X] T026 [P] Add validation in all TaskManager methods to handle invalid task IDs gracefully
- [X] T027 [P] Add validation in UI functions to handle invalid user inputs gracefully
- [X] T028 [P] Implement error display functions in src/ui.py for user-friendly error messages
- [X] T029 Add error handling in main application loop for keyboard interrupts and other exceptions
- [X] T030 Handle edge cases: empty task list, invalid inputs, and cancellation scenarios

## Phase 7: Testing

Unit tests for all components to ensure quality and reliability.

- [X] T031 Create tests/test_models.py to test Task validation and creation
- [X] T032 Create tests/test_task_manager.py to test all CRUD operations
- [X] T033 Test edge cases: empty list, invalid IDs, duplicate operations
- [X] T034 Verify error handling in tests

## Phase 8: Documentation and Polish

Final touches and documentation.

- [X] T035 Update README.md with project description and setup instructions
- [X] T036 Add usage instructions to README.md for all 5 operations
- [X] T037 Include WSL 2 setup instructions for Windows users in README.md
- [X] T038 Manual testing and validation of all features
- [X] T039 Verify all acceptance criteria are met

## Dependencies

**User Story Completion Order**: US1 → US2 → US3
- User Story 2 depends on foundational components from US1
- User Story 3 depends on foundational components from US1

## Parallel Execution Opportunities

**Within each user story**: UI functions, model methods, and service methods can often be developed in parallel as they work with different files and have minimal interdependencies.

**Across user stories**: After foundational components are in place, each user story can be developed somewhat independently since they build on the shared TaskManager and UI components.