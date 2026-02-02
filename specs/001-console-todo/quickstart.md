# Quickstart Guide: Phase I - In-Memory Python Console App

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup
1. Clone the repository
2. Navigate to the `phase-1` directory
3. Install dependencies:
   ```bash
   uv sync
   ```

## Running the Application
```bash
cd phase-1
uv run src/main.py
```

## Available Commands
Once the application starts, you'll see a menu with these options:
1. Add Task - Create a new todo task
2. View All Tasks - Display all tasks with their status
3. Update Task - Modify an existing task
4. Delete Task - Remove a task (with confirmation)
5. Toggle Complete Status - Mark task as complete/incomplete
6. Exit - Close the application

## Example Usage
1. Launch the application with `uv run src/main.py`
2. Select option 1 to add a task
3. Enter a title and optional description
4. Use option 2 to view your tasks
5. Continue using the menu to manage your tasks
6. Select option 6 to exit when done

## Running Tests
```bash
uv run pytest tests/
```

## Project Structure
```
phase-1/
├── src/
│   ├── main.py          # Entry point and CLI menu
│   ├── task_manager.py  # Business logic for task operations
│   ├── models.py        # Task data model
│   ├── ui.py            # User interface functions
│   └── utils.py         # Utility functions
├── tests/
│   ├── test_task_manager.py  # Task manager tests
│   └── test_models.py        # Model tests
├── pyproject.toml       # Project configuration
└── README.md            # Full documentation
```