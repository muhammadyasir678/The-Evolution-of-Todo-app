---
id: 1
title: "Create Todo Evolution Hackathon II Constitution"
stage: constitution
date_iso: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
link_spec: null
link_ticket: null
link_adr: null
link_pr: null

files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-create-todo-evolution-hackathon-ii.constitution.prompt.md"

tests_yaml:
  - "No tests needed for constitution creation"

prompt_text: |

  PROJECT NAME: Todo Evolution - Hackathon II

  PROJECT PURPOSE:
  Build a Todo application that evolves from console app to cloud-native AI chatbot using spec-driven development.

  CORE PRINCIPLES:
  - No manual coding - all code via Claude Code
  - Spec-driven: Specify → Plan → Tasks → Implement
  - Constitution created ONCE for entire project
  - One phase at a time, no skipping
  - All specs must be validated before implementation

  TECHNOLOGY STACK:
  - Phase I: Python 3.13+, UV
  - Phase II: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
  - Phase III: OpenAI ChatKit, Agents SDK, Official MCP SDK
  - Phase IV: Docker, Minikube, Helm, kubectl-ai, kagent
  - Phase V: Kafka, Dapr, AKS/GKE/DOKS, GitHub Actions

  PROJECT STRUCTURE:
  /
  ├── .spec-kit/
  ├── specs/
  │   ├── overview.md
  │   ├── features/
  │   ├── api/
  │   ├── database/
  │   └── ui/
  ├── phase-1/
  │   └── src/
  ├── phase-2/
  │   ├── frontend/
  │   └── backend/
  ├── phase-3/
  │   ├── frontend/
  │   ├── backend/
  │   └── mcp-server/
  ├── phase-4/
  │   ├── docker/
  │   └── helm-charts/
  ├── phase-5/
  │   ├── kafka/
  │   └── dapr/
  ├── AGENTS.md
  ├── CLAUDE.md
  └── README.md

  PHASES:
  - Phase I: In-Memory Python Console App
  - Phase II: Full-Stack Web Application
  - Phase III: AI-Powered Todo Chatbot
  - Phase IV: Local Kubernetes Deployment
  - Phase V: Advanced Cloud Deployment

  DEVELOPMENT RULES:
  - Each phase has its own folder
  - Specs written before any code
  - No jumping to next phase without completion
  - All implementations must reference Task IDs
  - Constitution never recreated

  QUALITY STANDARDS:
  - Clean code principles
  - Proper error handling
  - User input validation
  - Database indexing for performance
  - Stateless architecture for scalability
  - 90% test coverage target

response_text: |
  Created the project constitution for Todo Evolution - Hackathon II with the following key elements:

  1. Core Principles established:
     - No Manual Coding: All code must be generated via Claude Code
     - Spec-Driven Development: Follow Specify → Plan → Tasks → Implement sequence
     - Phase Sequentiality: Complete each phase before advancing
     - Single Constitution Rule: Created once and never fundamentally altered
     - Validation Before Implementation: Specs must be validated before implementation
     - Technology Stack Adherence: Fixed tech stack per phase

  2. Development Guidelines defined for the five-phase evolution
  3. Quality Standards established including 90% test coverage target
  4. Governance structure with version control and amendment procedures

  The constitution is version 1.0.0, ratified on 2026-01-24, and serves as the governing document for the entire project lifecycle.

outcome: |
  Successfully created the project constitution document that will guide the Todo Evolution - Hackathon II project from inception to completion across all five phases of development.

evaluation: |
  The constitution meets all requirements specified by the user, with clear principles, guidelines, and governance structure. It establishes the foundation for spec-driven development across all phases of the project.
---
