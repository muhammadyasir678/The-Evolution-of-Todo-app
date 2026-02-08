# Tasks: Kubernetes Minikube Deployment

**Input**: Design documents from `/specs/001-k8s-minikube-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase-4/`, `docker/`, `k8s/`, `helm-charts/`, `scripts/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T301 Create project structure per implementation plan in phase-4/
- [x] T302 Create subdirectories: docker/, k8s/, helm-charts/, scripts/ in phase-4/
- [x] T303 Create README.md and CLAUDE.md placeholders in phase-4/
- [x] T304 [P] Create docker/frontend.Dockerfile with multi-stage build
- [x] T305 [P] Create docker/backend.Dockerfile with multi-stage build
- [x] T306 [P] Create docker/mcp-server.Dockerfile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T307 Create docker/docker-compose.yml with frontend, backend, mcp-server services
- [x] T308 Create k8s/namespace.yaml defining namespace: todo-app
- [x] T309 Create k8s/configmap.yaml with non-sensitive configuration
- [x] T310 Create k8s/secret.yaml template with base64 encoding documentation
- [x] T311 Create scripts/build-images.sh with Minikube Docker environment setup
- [x] T312 Create scripts/deploy-minikube.sh with namespace creation and Helm installation
- [x] T313 [P] Create helm-charts/todo-app/ directory structure with Chart.yaml and values.yaml

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Developer Deploys Application to Minikube (Priority: P1) 🎯 MVP

**Goal**: Enable developers to deploy the chatbot application to a local Kubernetes cluster using Minikube with a single command

**Independent Test**: Can be fully tested by running a Helm install command on a Minikube cluster and verifying that all services are running and accessible. Delivers the ability to run the full application stack in Kubernetes locally

### Implementation for User Story 1

- [x] T314 [P] [US1] Create k8s/frontend-deployment.yaml with 2 replicas and proper configuration
- [x] T315 [P] [US1] Create k8s/frontend-service.yaml with NodePort type and port 30000
- [x] T316 [P] [US1] Create k8s/backend-deployment.yaml with 2 replicas and health checks
- [x] T317 [P] [US1] Create k8s/backend-service.yaml with ClusterIP type and port 8000
- [x] T318 [P] [US1] Create k8s/mcp-deployment.yaml with 1 replica and proper configuration
- [x] T319 [P] [US1] Create k8s/mcp-service.yaml with ClusterIP type
- [ ] T320 [US1] Setup Minikube environment with proper installation steps and cluster start
- [ ] T321 [US1] Build Docker images in Minikube with eval $(minikube docker-env) and build-images.sh
- [ ] T322 [US1] Deploy application to Minikube with secrets creation and deploy-minikube.sh
- [ ] T323 [US1] Test application on Minikube with access verification and functionality testing

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Containerize Application Components (Priority: P2)

**Goal**: Create optimized Docker images for frontend, backend, and MCP server components with multi-stage builds and health checks

**Independent Test**: Can be tested by building the Docker images locally and verifying they run correctly with appropriate environment configurations. Delivers portable, optimized containers for the application components

### Implementation for User Story 2

- [x] T324 [P] [US2] Implement multi-stage build for frontend.Dockerfile with builder and production stages
- [x] T325 [P] [US2] Implement multi-stage build for backend.Dockerfile with uv dependency installation
- [x] T326 [P] [US2] Implement MCP server Dockerfile with proper Python dependencies
- [x] T327 [P] [US2] Add health checks to all Dockerfiles
- [ ] T328 [US2] Optimize Docker images for smaller size with proper layer caching
- [ ] T329 [US2] Test Docker Compose locally with .env file and full functionality verification

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Configure Kubernetes Resources (Priority: P3)

**Goal**: Define proper Kubernetes manifests for deployments, services, ConfigMaps, and Secrets that follow best practices

**Independent Test**: Can be tested by applying individual Kubernetes manifests to a cluster and verifying they function as expected. Delivers properly configured Kubernetes resources for reliable application operation

### Implementation for User Story 3

- [x] T330 [P] [US3] Add resource requests and limits to all deployment manifests
- [x] T331 [P] [US3] Add readiness and liveness probes to frontend and backend deployments
- [x] T332 [P] [US3] Implement secure handling of sensitive data in secrets
- [ ] T333 [US3] Validate Kubernetes manifests follow best practices for production readiness
- [ ] T334 [US3] Test individual Kubernetes resources with kubectl apply and verification

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Deploy via Helm Chart (Priority: P2)

**Goal**: Package all Kubernetes resources into a Helm chart with configurable values that supports different environments

**Independent Test**: Can be tested by installing the Helm chart with different configuration values and verifying it deploys the application correctly. Delivers simplified application deployment and management

### Implementation for User Story 4

- [x] T335 [P] [US4] Copy all k8s/*.yaml to helm-charts/todo-app/templates/
- [x] T336 [P] [US4] Parameterize Kubernetes manifests with {{ .Values.* }} syntax
- [x] T337 [P] [US4] Create _helpers.tpl for reusable template functions
- [x] T338 [US4] Support replicas, image tags, resources from values.yaml
- [ ] T339 [US4] Test Helm chart installation with default and custom values
- [ ] T340 [US4] Test Helm upgrade functionality without downtime

**Checkpoint**: At this point, all user stories should be integrated and working together

---

## Phase 7: User Story 5 - Use AI-Assisted Development Tools (Priority: P3)

**Goal**: Leverage AI tools like Docker AI (Gordon), kubectl-ai, and kagent for various development and operational tasks

**Independent Test**: Can be tested by using AI tools to generate Dockerfiles, Kubernetes manifests, and troubleshoot issues. Delivers increased developer productivity and reduced configuration errors

### Implementation for User Story 5

- [x] T341 [P] [US5] Document Docker AI (Gordon) commands used for Dockerfile optimization
- [x] T342 [P] [US5] Document kubectl-ai commands used for Kubernetes operations
- [x] T343 [P] [US5] Document kagent commands used for troubleshooting
- [ ] T344 [US5] Integrate AI tools into deployment workflow where applicable
- [ ] T345 [US5] Test AI-assisted operations and document results

**Checkpoint**: All user stories should now be enhanced with AI-assisted capabilities

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T346 [P] Update phase-4/README.md with prerequisites, build, and deployment instructions
- [x] T347 [P] Update phase-4/CLAUDE.md with implementation notes
- [ ] T348 [P] Create demo and verification documentation with video showing deployment process
- [ ] T349 Troubleshooting and optimization with log checking and resource verification
- [x] T350 Run quickstart.md validation to ensure all steps work as documented

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Builds on previous stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Enhances all previous stories

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
# Launch all deployment manifests for User Story 1 together:
Task: "Create k8s/frontend-deployment.yaml with 2 replicas and proper configuration"
Task: "Create k8s/frontend-service.yaml with NodePort type and port 30000"
Task: "Create k8s/backend-deployment.yaml with 2 replicas and health checks"
Task: "Create k8s/backend-service.yaml with ClusterIP type and port 8000"
Task: "Create k8s/mcp-deployment.yaml with 1 replica and proper configuration"
Task: "Create k8s/mcp-service.yaml with ClusterIP type"
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