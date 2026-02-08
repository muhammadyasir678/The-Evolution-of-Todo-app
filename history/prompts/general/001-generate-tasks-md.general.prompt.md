---
id: 001
title: Generate-tasks-md
stage: tasks
date: 2026-02-08
surface: agent
model: Qwen
feature: none
branch: main
user: system
command: sp.tasks
labels: ["tasks", "kubernetes", "minikube", "deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/f/The-Evolution-of-Todo-app/specs/001-k8s-minikube-deployment/tasks.md
tests:
 - /mnt/f/The-Evolution-of-Todo-app/specs/001-k8s-minikube-deployment/tasks.md
---

## Prompt

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: /sp.tasks PHASE: Phase IV - Local Kubernetes Deployment (Minikube) BASE: Approved speckit.plan for Phase IV TASKS: T-301: Create Project Structure - Create phase-4/ directory - Create subdirectories: docker/, k8s/, helm-charts/, scripts/ - Create README.md and CLAUDE.md placeholders - Reference: speckit.plan §Project Structure T-302: Create Frontend Dockerfile - Create docker/frontend.Dockerfile - Implement multi-stage build (builder + production) - Stage 1: Install dependencies and build Next.js - Stage 2: Copy build artifacts, production dependencies only - Expose port 3000 - Add health check - Optimize for smaller image size - Reference: speckit.plan §Frontend Dockerfile T-303: Create Backend Dockerfile - Create docker/backend.Dockerfile - Implement multi-stage build (builder + production) - Stage 1: Install Python dependencies with uv - Stage 2: Copy dependencies and application code - Expose port 8000 - Add health check endpoint - Optimize for smaller image size - Reference: speckit.plan §Backend Dockerfile T-304: Create MCP Server Dockerfile - Create docker/mcp-server.Dockerfile - Install Python dependencies with uv - Copy MCP server code - Configure entry point - Reference: speckit.plan §MCP Server Dockerfile T-305: Create Docker Compose File - Create docker/docker-compose.yml - Define services: frontend, backend, mcp-server - Configure service dependencies - Set environment variables from .env - Map ports for local access - Reference: speckit.plan §docker-compose.yml T-306: Test Docker Compose Locally - Create .env file with required variables - Run: docker-compose -f docker/docker-compose.yml up - Verify all services start without errors - Test frontend accessible at localhost:3000 - Test backend API at localhost:8000 - Test full chat functionality - Reference: speckit.plan §Docker Testing T-307: Create Kubernetes Namespace Manifest - Create k8s/namespace.yaml - Define namespace: todo-app - Reference: speckit.plan §Namespace T-308: Create Kubernetes ConfigMap - Create k8s/configmap.yaml - Add non-sensitive configuration - Include: NEXT_PUBLIC_API_URL, ports - Reference: speckit.plan §ConfigMap T-309: Create Kubernetes Secret Manifest - Create k8s/secret.yaml (template only, values separate) - Define secret: todo-secrets - Keys: DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET - Document base64 encoding requirement - Reference: speckit.plan §Secret T-310: Create Frontend Kubernetes Deployment - Create k8s/frontend-deployment.yaml - Define Deployment with 2 replicas - Configure container with image, port, env from ConfigMap/Secret - Add resource requests and limits - Add readiness and liveness probes - Reference: speckit.plan §Frontend Deployment T-311: Create Frontend Kubernetes Service - Create k8s/frontend-service.yaml - Define Service type: NodePort - NodePort: 30000 - Selector matches frontend pods - Reference: speckit.plan §Services T-312: Create Backend Kubernetes Deployment - Create k8s/backend-deployment.yaml - Define Deployment with 2 replicas - Configure container with image, port, env from ConfigMap/Secret - Add resource requests and limits - Add readiness and liveness probes (HTTP /health) - Reference: speckit.plan §Backend Deployment T-313: Create Backend Kubernetes Service - Create k8s/backend-service.yaml - Define Service type: ClusterIP - Port: 8000 - Selector matches backend pods - Reference: speckit.plan §Services T-314: Create MCP Server Kubernetes Deployment - Create k8s/mcp-deployment.yaml - Define Deployment with 1 replica - Configure container with image, env from Secret - Add resource requests and limits - Reference: speckit.plan §MCP Server Deployment T-315: Create MCP Server Kubernetes Service - Create k8s/mcp-service.yaml - Define Service type: ClusterIP - Selector matches MCP pods - Reference: speckit.plan §Services T-316: Create Helm Chart Structure - Create helm-charts/todo-app/ directory - Create Chart.yaml with metadata - Create values.yaml with parameters - Create templates/ directory - Reference: speckit.plan §Helm Chart Structure T-317: Create Helm Chart Templates - Copy all k8s/*.yaml to templates/ - Parameterize with {{ .Values.* }} syntax - Support replicas, image tags, resources from values.yaml - Create _helpers.tpl for reusable template functions - Reference: speckit.plan §Templates T-318: Create Build Script - Create scripts/build-images.sh - Set Minikube Docker environment - Build all three images (frontend, backend, mcp-server) - Tag images appropriately - Make script executable - Reference: speckit.plan §Build Images T-319: Create Deployment Script - Create scripts/deploy-minikube.sh - Create namespace if not exists - Create secrets from environment variables - Install Helm chart with values - Display deployment status - Show access instructions - Make script executable - Reference: speckit.plan §Deploy with Helm T-320: Setup Minikube Environment - Document Minikube installation steps - Start Minikube cluster - Enable necessary addons (ingress if needed) - Verify cluster is running - Reference: speckit.plan §Setup T-321: Build Docker Images in Minikube - Set Minikube Docker environment: eval $(minikube docker-env) - Run build-images.sh script - Verify images created: docker images | grep todo - Reference: speckit.plan §Build Images T-322: Deploy Application to Minikube - Create Kubernetes secrets manually with actual values - Run deploy-minikube.sh script - Wait for all pods to be Running - Check pod status: kubectl get pods -n todo-app - Reference: speckit.plan §Deploy with Helm T-323: Test Application on Minikube - Get Minikube IP: minikube ip - Access frontend via NodePort: http://<minikube-ip>:30000 - Or use: minikube service frontend-service -n todo-app - Test sign up/sign in functionality - Test chat interface - Test task management via natural language - Verify backend and MCP communication - Reference: speckit.plan §Access Application T-324: Use AI DevOps Tools - Use Gordon for Docker operations (if available): "docker ai 'optimize my Dockerfile'" - Use kubectl-ai: "kubectl-ai 'show pods in todo-app namespace'" - Use kagent: "kagent 'check cluster health'" - Document all AI commands used - Reference: speckit.plan §AI DevOps Commands T-325: Troubleshooting and Optimization - Check logs if any pod fails: kubectl logs <pod-name> -n todo-app - Describe pods for events: kubectl describe pod <pod-name> -n todo-app - Verify resource usage: kubectl top pods -n todo-app - Fix any issues and redeploy - Reference: speckit.plan §Troubleshooting Guide T-326: Documentation - Update phase-4/README.md with: - Prerequisites (Docker, Minikube, kubectl, Helm) - Build instructions - Deployment instructions - How to access application - Troubleshooting guide - AI DevOps commands used - Update CLAUDE.md with implementation notes - Reference: speckit.specify §Acceptance Criteria T-327: Create Demo and Verification - Create demo video showing: - Minikube deployment process - Application running on K8s - Chat functionality working - kubectl commands showing pods/services - Verify all acceptance criteria met - Reference: speckit.specify §Acceptance Criteria

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.