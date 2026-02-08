# Tasks: Advanced Cloud Deployment

**Input**: Design documents from `/specs/002-advanced-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase-5/`, `services/`, `frontend/`, `backend/`, `k8s/`, `helm-charts/`, `scripts/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T401 Create phase-5/ directory structure with services/, frontend/, backend/, k8s/, helm-charts/, scripts/ subdirectories
- [x] T402 Create services/recurring-task-service/ directory with src/, Dockerfile, pyproject.toml
- [x] T403 Create services/notification-service/ directory with src/, Dockerfile, pyproject.toml
- [x] T404 Create services/audit-service/ directory with src/, Dockerfile, pyproject.toml
- [x] T405 Create services/websocket-service/ directory with src/, Dockerfile, pyproject.toml
- [ ] T406 [P] Create frontend/components/TaskPriority.tsx
- [ ] T407 [P] Create frontend/components/TaskTags.tsx
- [ ] T408 [P] Create frontend/components/TaskDueDate.tsx
- [ ] T409 [P] Create frontend/components/TaskRecurrence.tsx
- [ ] T410 [P] Create frontend/components/TaskFilters.tsx
- [ ] T411 [P] Create frontend/components/TaskSearch.tsx

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T412 Extend backend/app/models.py with new Task model fields (priority, tags, due_date, reminder_time, recurrence_pattern, recurrence_interval, parent_task_id)
- [x] T413 Create database migration script for new Task model columns
- [x] T414 Add indexes on priority, due_date, tags in the database
- [x] T415 Create AuditLog model in backend/app/models.py with fields: id, user_id, task_id, action, details (jsonb), timestamp
- [x] T416 Create database migration script for AuditLog model
- [x] T417 Create k8s/kafka/strimzi-kafka.yaml with Kafka cluster definition and 3 topics: task-events, reminders, task-updates
- [x] T418 Create backend/app/kafka_producer.py with KafkaProducer initialization and publish functions
- [x] T419 Create k8s/dapr/pubsub.yaml with Kafka pub/sub component configuration
- [x] T420 Create k8s/dapr/statestore.yaml with PostgreSQL state store configuration
- [x] T421 Create k8s/dapr/secretstore.yaml with Kubernetes secrets store configuration
- [x] T422 Create helm-charts/todo-app-v5/ directory with Chart.yaml, values.yaml, and templates/ subdirectory

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Recurring Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create recurring tasks with daily, weekly, or monthly patterns and automatically generate next occurrences when completed

**Independent Test**: A user can create a "Weekly meeting" task with a weekly recurrence pattern, complete it, and verify that the system automatically creates the next week's occurrence.

### Implementation for User Story 1

- [x] T423 [P] [US1] Create Recurring Task Service consumer in services/recurring-task-service/src/main.py
- [x] T424 [P] [US1] Implement Kafka consumer logic for task-events topic in Recurring Task Service
- [x] T425 [P] [US1] Implement recurrence pattern logic (daily, weekly, monthly) in Recurring Task Service
- [x] T426 [US1] Update backend/app/routes/tasks.py to publish to task-events on task completion
- [x] T427 [US1] Create k8s/services/recurring-task-deployment.yaml with Dapr annotations
- [x] T428 [US1] Create k8s/services/recurring-task-service.yaml for internal service
- [ ] T429 [US1] Update frontend TaskForm component to include recurrence fields
- [ ] T430 [US1] Test recurring task creation and automatic next occurrence generation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Due Date Reminders with Notifications (Priority: P1)

**Goal**: Allow users to set due dates and reminders for tasks, with notifications sent via browser or email when reminder time arrives

**Independent Test**: A user can set a task with a due date and 1-hour reminder, and receive a notification 1 hour before the deadline.

### Implementation for User Story 2

- [x] T431 [P] [US2] Create Notification Service consumer in services/notification-service/src/main.py
- [x] T432 [P] [US2] Implement Kafka consumer logic for reminders topic in Notification Service
- [x] T433 [P] [US2] Integrate Web Push API for browser notifications in Notification Service
- [x] T434 [P] [US2] Integrate email service (SendGrid or AWS SES) in Notification Service
- [x] T435 [US2] Update backend/app/routes/tasks.py to publish to reminders topic when due_date and reminder_time set
- [x] T436 [US2] Create k8s/services/notification-deployment.yaml with Dapr annotations
- [x] T437 [US2] Create k8s/services/notification-service.yaml for internal service
- [ ] T438 [US2] Update frontend TaskForm component to include due date and reminder fields
- [ ] T439 [US2] Test due date reminder scheduling and delivery

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Enhanced Task Organization (Priority: P2)

**Goal**: Enable users to assign priorities, add tags to tasks, and filter/sort tasks based on these attributes

**Independent Test**: A user can assign high priority to a task, tag it as "work", and filter the task list to show only high priority "work" tasks.

### Implementation for User Story 3

- [x] T440 [P] [US3] Create Task Priority component in frontend/components/TaskPriority.tsx
- [x] T441 [P] [US3] Create Task Tags component in frontend/components/TaskTags.tsx
- [x] T442 [P] [US3] Create Task Filters component in frontend/components/TaskFilters.tsx
- [x] T443 [US3] Update backend/app/routes/tasks.py to support filtering by priority, tags, status, due date range
- [x] T444 [US3] Implement sort functionality in backend/app/routes/tasks.py (due date, priority, created date, title)
- [ ] T445 [US3] Update frontend task list to support filtering and sorting
- [ ] T446 [US3] Implement sort persistence in frontend using local storage
- [x] T447 [US3] Create Task Search component in frontend/components/TaskSearch.tsx
- [x] T448 [US3] Implement instant search functionality in frontend
- [ ] T449 [US3] Test filtering, sorting, and search functionality

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Event-Driven Real-Time Sync (Priority: P2)

**Goal**: Enable real-time synchronization of task changes across all devices where a user is logged in

**Independent Test**: A user can create a task on their desktop browser and immediately see it appear in their mobile application.

### Implementation for User Story 4

- [x] T450 [P] [US4] Create WebSocket Service in services/websocket-service/src/main.py
- [x] T451 [P] [US4] Implement WebSocket server with FastAPI in WebSocket Service
- [x] T452 [P] [US4] Implement Kafka consumer for task-updates topic in WebSocket Service
- [x] T453 [P] [US4] Maintain user WebSocket connections in WebSocket Service
- [x] T454 [US4] Create k8s/services/websocket-deployment.yaml with Dapr annotations
- [x] T455 [US4] Create k8s/services/websocket-service.yaml with LoadBalancer type
- [x] T456 [US4] Update backend/app/routes/tasks.py to publish to task-updates topic on create/update/delete/complete
- [ ] T457 [US4] Integrate WebSocket connection in frontend to WebSocket service
- [ ] T458 [US4] Implement real-time task updates in frontend via WebSocket
- [ ] T459 [US4] Test real-time synchronization across multiple devices

**Checkpoint**: At this point, all user stories should be integrated and working together

---

## Phase 7: User Story 5 - Cloud Deployment and Scaling (Priority: P3)

**Goal**: Enable deployment of the application to cloud Kubernetes with auto-scaling, monitoring, and CI/CD pipeline

**Independent Test**: Developers can push code changes to the main branch and verify that the CI/CD pipeline automatically builds, tests, and deploys the application to the cloud environment.

### Implementation for User Story 5

- [x] T460 [P] [US5] Create k8s/services/audit-deployment.yaml with Dapr annotations
- [x] T461 [P] [US5] Create k8s/services/audit-service.yaml for internal service
- [x] T462 [P] [US5] Create Audit Service consumer in services/audit-service/src/main.py
- [x] T463 [P] [US5] Implement Kafka consumer logic for task-events topic in Audit Service
- [x] T464 [US5] Update backend to publish events via Dapr HTTP API instead of direct Kafka
- [x] T465 [US5] Update all services to consume via Dapr subscriptions using @dapr_app.subscribe decorator
- [x] T466 [US5] Implement Dapr Jobs API for scheduling reminders in backend
- [x] T467 [US5] Create .github/workflows/deploy.yml with CI/CD pipeline
- [ ] T468 [US5] Set up cloud Kubernetes cluster (AKS, GKE, or DOKS)
- [ ] T469 [US5] Set up managed Kafka (Redpanda Cloud or Confluent Cloud)
- [ ] T470 [US5] Update Dapr pubsub.yaml for cloud Kafka with authentication
- [ ] T471 [US5] Install Dapr on cloud K8s cluster
- [ ] T472 [US5] Deploy application to cloud via CI/CD pipeline
- [ ] T473 [US5] Configure monitoring and logging with alerts

**Checkpoint**: At this point, all user stories should be deployed and working in cloud environment

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T474 [P] Update phase-5/README.md with architecture overview and deployment instructions
- [x] T475 [P] Create CLAUDE.md with implementation notes for Phase V
- [x] T476 [P] Update helm-charts/todo-app-v5/values.yaml with all service configurations
- [x] T477 [P] Create scripts/deploy-minikube-v5.sh for local deployment
- [x] T478 [P] Create scripts/deploy-cloud.sh for cloud deployment
- [x] T479 Unit tests for new services (Recurring Task, Notification, Audit, WebSocket)
- [x] T480 Integration tests for event-driven flows
- [x] T481 Load testing for performance validation
- [x] T482 Create demo video demonstrating all advanced features
- [x] T483 Run quickstart.md validation to ensure all steps work as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Builds on previous stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Integrates all previous stories

### Within Each User Story

- Core implementation before integration
- Individual components before full deployment
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create Recurring Task Service consumer in services/recurring-task-service/src/main.py"
Task: "Implement Kafka consumer logic for task-events topic in Recurring Task Service"
Task: "Implement recurrence pattern logic (daily, weekly, monthly) in Recurring Task Service"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence