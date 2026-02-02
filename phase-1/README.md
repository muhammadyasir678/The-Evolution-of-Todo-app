# Todo Console Application

A simple console-based todo application with in-memory storage built in Python.

## Features
- Add new todo tasks
- View all tasks with status indicators
- Update existing tasks
- Delete tasks with confirmation
- Mark tasks as complete/incomplete

## Setup

1. Make sure you have Python 3.13+ installed
2. Install UV package manager if you don't have it:
   ```
   pip install uv
   ```
3. Clone the repository and navigate to the phase-1 directory
4. Install dependencies:
   ```
   uv sync
   ```

## Usage

Run the application:
```
uv run python src/main.py
```

Or if installed as a package:
```
uv run todo-app
```

### Available Operations
1. **Add Task**: Create a new todo task with a title and optional description
2. **View All Tasks**: Display all tasks with ID, status indicator, title, and description
3. **Update Task**: Modify an existing task's title and/or description
4. **Delete Task**: Remove a task with confirmation prompt
5. **Toggle Complete Status**: Mark a task as complete/incomplete
6. **Exit**: Close the application

## Supported Platforms
- Windows (with WSL 2)
- macOS
- Linux

### WSL 2 Setup Instructions (for Windows users)
1. Install WSL 2 by following Microsoft's official guide
2. Install a Linux distribution (Ubuntu recommended)
3. Install Python 3.13+ in your WSL environment
4. Install UV package manager: `pip install uv`
5. Clone and run the application as described above

## Architecture
- `src/models.py` - Task data model
- `src/task_manager.py` - Business logic for CRUD operations
- `src/ui.py` - User interface functions
- `src/utils.py` - Utility functions
- `src/main.py` - Main application entry point

## Testing
Run the unit tests with:
```
uv run pytest tests/
```