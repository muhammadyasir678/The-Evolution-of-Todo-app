---
name: python-console-dev
description: Build clean, robust command-line Python applications using Python 3.13+, in-memory CRUD, and modern project practices. Use for CLI-based tools and utilities.
---

# Python Console Development

## Instructions

1. **Project setup**
   - Use Python **3.13+**
   - Initialize project using **UV** for dependency and environment management
   - Follow a clear, modular project structure (`src/`, `tests/`, `pyproject.toml`)

2. **Application architecture**
   - Separate concerns: CLI layer, business logic, and data models
   - Use in-memory data structures (lists, dicts) as the primary datastore
   - Implement full **CRUD operations** (Create, Read, Update, Delete)

3. **CLI interface**
   - Design clear commands and subcommands
   - Validate all user inputs (types, ranges, required fields)
   - Provide helpful error messages and usage hints
   - Support interactive and non-interactive (arguments-based) usage

4. **Code quality**
   - Follow **PEP 8** style guidelines
   - Use meaningful variable, function, and module names
   - Write small, testable functions
   - Add docstrings for public functions and modules

5. **Business logic & models**
   - Define explicit data models (dataclasses or typed dictionaries)
   - Encapsulate rules and validations in the business layer
   - Avoid placing logic directly in the CLI handlers

## Best Practices

- Keep CLI commands simple and predictable
- Prefer composition over deeply nested conditionals
- Fail fast on invalid input
- Use type hints throughout the codebase
- Keep the main entry point minimal
- Design for easy future migration to persistent storage

## Example Structure

```text
python-console-dev/
├── pyproject.toml
├── src/
│   └── app/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── service.py
│       └── repository.py
└── tests/
    └── test_service.py
