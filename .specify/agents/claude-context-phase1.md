# Claude Agent Context: Phase I Console Todo App

## Project Context
- Building a Python console application for todo management
- In-memory storage using dictionaries
- No external dependencies beyond standard library
- Target Python 3.13+

## Architecture
- Modular design with separation of concerns
- Models module for data representation
- Task manager for business logic
- UI module for user interaction
- Utils for helper functions

## Key Components
- Task class with id, title, description, completed status, and creation timestamp
- TaskManager class with CRUD operations
- CLI menu system with 6 main options
- Input validation and error handling

## Implementation Notes
- All code must follow PEP 8 standards
- Use type hints for all function signatures
- Implement proper error handling with user-friendly messages
- Auto-incrementing IDs for tasks
- Confirmation prompts for destructive operations