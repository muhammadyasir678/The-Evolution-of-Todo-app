---
name: qa-testing
description: Design and implement comprehensive quality assurance testing strategies across backend, frontend, AI agents, and infrastructure. Use for ensuring reliability, correctness, and deployment confidence.
---

# QA Testing Skill

## Instructions

1. **Unit Testing**
   - Write unit tests for Python using `pytest` and `unittest`
   - Write unit tests for TypeScript using `Jest` or `Vitest`
   - Ensure high coverage for core business logic
   - Test edge cases and error handling paths

2. **Integration Testing**
   - Create integration tests for REST and GraphQL API endpoints
   - Validate request/response schemas and status codes
   - Test database interactions and external service integrations
   - Use isolated test environments

3. **AI Agent & Tool Testing**
   - Validate AI agent behavior against expected prompts and outputs
   - Test tool invocation correctness and parameter passing
   - Simulate failure scenarios and fallback logic
   - Assert deterministic behavior where applicable

4. **End-to-End (E2E) Testing**
   - Implement E2E tests for full-stack applications
   - Cover user journeys from UI to backend
   - Validate authentication, authorization, and workflows
   - Use browser automation tools where required

5. **Container & Deployment Testing**
   - Test containerized applications using Docker-based test setups
   - Validate container health checks and startup behavior
   - Ensure environment variables and secrets are correctly wired

6. **Kubernetes Validation**
   - Validate Kubernetes manifests and Helm charts
   - Test pod readiness/liveness probes
   - Verify service discovery, scaling, and rollout behavior
   - Detect misconfigurations before production deployment

7. **Test Data & Mocks**
   - Create reusable test data fixtures
   - Mock external services and APIs
   - Use stubs and fakes to isolate test scopes
   - Ensure test data is deterministic and reproducible

8. **Acceptance Criteria Validation**
   - Translate acceptance criteria into automated tests
   - Validate functional and non-functional requirements
   - Ensure tests reflect real business expectations
   - Provide clear pass/fail signals for release decisions

## Best Practices
- Follow the testing pyramid (unit → integration → E2E)
- Keep tests isolated, repeatable, and deterministic
- Fail fast with clear error messages
- Automate tests in CI/CD pipelines
- Treat tests as first-class production code
- Prefer readability and intent over cleverness

## Example Structure

### Python Unit Test
```python
def test_calculate_total_with_tax():
    total = calculate_total(amount=100, tax_rate=0.1)
    assert total == 110
