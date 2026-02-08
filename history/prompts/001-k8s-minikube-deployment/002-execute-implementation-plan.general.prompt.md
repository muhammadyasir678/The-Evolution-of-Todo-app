---
id: 002
title: Execute-implementation-plan
stage: green
date: 2026-02-08
surface: agent
model: Qwen
feature: k8s-minikube-deployment
branch: main
user: system
command: sp.implement
labels: ["kubernetes", "minikube", "deployment", "docker", "helm", "ai-tools"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/README.md
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/CLAUDE.md
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/docker/frontend.Dockerfile
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/docker/backend.Dockerfile
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/docker/mcp-server.Dockerfile
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/docker/docker-compose.yml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/namespace.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/configmap.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/secret.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/frontend-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/frontend-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/backend-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/backend-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/mcp-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/k8s/mcp-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/Chart.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/values.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/_helpers.tpl
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/namespace.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/configmap.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/secret.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/frontend-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/frontend-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/backend-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/backend-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/mcp-deployment.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/helm-charts/todo-app/templates/mcp-service.yaml
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/scripts/build-images.sh
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/scripts/deploy-minikube.sh
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/quickstart.md
 - /mnt/f/The-Evolution-of-Todo-app/phase-4/AI_TOOLS_DOCUMENTATION.md
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

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc* exists → create/verify .eslintignore
   - Check if eslint.config.* exists → ensure the config's `ignores` entries cover required patterns
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

7. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

8. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

9. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/sp.tasks` first to regenerate the task list.

---

/sp.implement /sp.implement

PHASE: Phase IV - Local Kubernetes Deployment (Minikube)

BASE: Approved speckit.tasks for Phase IV

AGENT ASSIGNMENTS:

T-301: DevOps Engineer
T-302: DevOps Engineer
T-303: DevOps Engineer
T-304: DevOps Engineer
T-305: DevOps Engineer
T-306: QA & Testing + DevOps Engineer
T-307: DevOps Engineer
T-308: DevOps Engineer
T-309: DevOps Engineer
T-310: DevOps Engineer
T-311: DevOps Engineer
T-312: DevOps Engineer
T-313: DevOps Engineer
T-314: DevOps Engineer
T-315: DevOps Engineer
T-316: DevOps Engineer
T-317: DevOps Engineer
T-318: DevOps Engineer
T-319: DevOps Engineer
T-320: DevOps Engineer
T-321: DevOps Engineer
T-322: DevOps Engineer
T-323: QA & Testing
T-324: DevOps Engineer
T-325: DevOps Engineer + QA & Testing
T-326: DevOps Engineer
T-327: QA & Testing + DevOps Engineer

IMPLEMENTATION INSTRUCTIONS:

DevOps Engineer will execute tasks in sequence with some parallelization.

Dependency Order:
- T-301 (project structure)
- T-302, T-303, T-304, T-305 (parallel - Docker files)
- T-306 (test Docker compose)
- T-307, T-308, T-309 (parallel - K8s config)
- T-310, T-311 (sequence - frontend K8s)
- T-312, T-313 (sequence - backend K8s)
- T-314, T-315 (sequence - MCP K8s)
- T-316, T-317 (sequence - Helm chart)
- T-318, T-319 (parallel - scripts)
- T-320 (Minikube setup)
- T-321 (build images)
- T-322 (deploy)
- T-323 (test deployment)
- T-324 (AI DevOps tools)
- T-325 (troubleshoot)
- T-326 (documentation)
- T-327 (demo)

Each task implementation must:
- Reference Task ID in code comments
- Follow speckit.plan architecture exactly
- Use multi-stage builds for Docker optimization
- Include proper health checks
- Set appropriate resource limits
- Use Helm for parameterization

Critical Requirements:
- Docker images must be built in Minikube Docker environment
- All secrets must be created separately (not in manifests)
- Services must use correct types (NodePort for frontend, ClusterIP for internal)
- Helm chart must parameterize all configurable values
- Health probes required for all deployments
- Use kubectl-ai and kagent for AI-assisted operations
- Document all Gordon/kubectl-ai/kagent commands used

EXIT CRITERIA:
- All Dockerfiles created with multi-stage builds
- docker-compose.yml functional locally
- All Kubernetes manifests created
- Helm chart packages entire application
- Minikube cluster running
- All images built in Minikube environment
- Application deployed via Helm
- All pods in Running state (verify with: kubectl get pods -n todo-app)
- Frontend accessible via browser
- Backend and MCP server communicating
- Full chat functionality working on Kubernetes
- AI DevOps tools (Gordon, kubectl-ai, kagent) used and documented
- README with complete instructions
- Demo video created

VERIFICATION CHECKLIST:
□ phase-4/ directory structure created
□ frontend.Dockerfile with multi-stage build
□ backend.Dockerfile with multi-stage build
□ mcp-server.Dockerfile created
□ docker-compose.yml working locally
□ All K8s manifests created (namespace, configmap, secret, deployments, services)
□ Helm chart structure created
□ Helm templates parameterized
□ build-images.sh script created
□ deploy-minikube.sh script created
□ Minikube started and running
□ Docker environment set to Minikube
□ All three images built successfully
□ Secrets created in K8s
□ Helm chart installed
□ All pods Running: kubectl get pods -n todo-app
□ Frontend accessible at http://<minikube-ip>:30000
□ Services resolving: kubectl get svc -n todo-app
□ Sign up/sign in working
□ Chat interface functional
□ Task operations via chat working
□ Gordon commands documented (if available)
□ kubectl-ai commands used and documented
□ kagent commands used and documented
□ README complete with setup steps
□ Demo video created

Begin implementation with T-301 (project structure).