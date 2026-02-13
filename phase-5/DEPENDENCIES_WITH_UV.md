# Dependency Management with UV

This document explains how to manage dependencies using `uv` for the Phase V Advanced Cloud Deployment project.

## Overview

We've migrated from Poetry to `uv` for faster dependency resolution and installation. `uv` is an extremely fast Python package installer and resolver, written in Rust.

## Project Structure

The Phase V project consists of multiple services, each with its own dependency requirements:

- `backend/` - Main backend API service
- `services/recurring-task-service/` - Service for handling recurring tasks
- `services/notification-service/` - Service for handling notifications
- `services/audit-service/` - Service for audit logging
- `services/websocket-service/` - Service for real-time WebSocket connections

## Installing Dependencies

### Prerequisites

Make sure you have `uv` installed:

```bash
# Install uv
pip install uv
# Or using the standalone installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### For a Single Service

Navigate to the service directory and install dependencies:

```bash
cd phase-5/backend
uv sync  # Creates a virtual environment and installs dependencies from pyproject.toml
```

Or if using requirements.txt:

```bash
cd phase-5/backend
uv pip install -r requirements.txt
```

### For All Services

Use the provided script to install dependencies for all services:

```bash
bash scripts/install-dependencies-with-uv.sh
```

## Adding New Dependencies

### To a pyproject.toml-based project:

```bash
cd <service-directory>
uv add <package-name>
```

### To a requirements.txt-based project:

Add the package to the requirements.txt file and run:

```bash
cd <service-directory>
uv pip install -r requirements.txt
```

## Creating Virtual Environments

`uv` can create virtual environments quickly:

```bash
cd <service-directory>
uv venv  # Creates a virtual environment in .venv/
source .venv/bin/activate  # Activate the environment
```

## Updating Dependencies

### For pyproject.toml-based projects:

```bash
cd <service-directory>
uv sync --locked  # Installs dependencies as specified in uv.lock
uv lock --upgrade  # Updates the lock file with latest compatible versions
```

### For requirements.txt-based projects:

```bash
# To update all packages to latest compatible versions
uv pip install -r requirements.txt --upgrade
```

## Benefits of Using UV

1. **Speed**: `uv` is significantly faster than pip and Poetry for dependency resolution and installation
2. **Compatibility**: Fully compatible with existing pip and Poetry workflows
3. **Lock files**: Generates lock files for reproducible builds
4. **Virtual environments**: Fast virtual environment creation and management

## Migration Notes

We've converted from Poetry to `uv` for the following reasons:
- Faster dependency resolution and installation
- Better performance in CI/CD environments
- Simplified dependency management workflow
- Improved lock file generation and management

The migration involved:
1. Converting pyproject.toml files from Poetry format to standard format
2. Creating requirements.txt files where needed
3. Updating installation scripts to use `uv`
4. Generating lock files for reproducible builds