---
id: "001"
title: "Fix Database Connection Issue in Backend"
stage: "general"
date_iso: "2026-01-29"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "001-full-stack-auth"
user: "user"
command: "resolve-backend-error"
labels: ["database", "connection", "environment", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "/mnt/f/The-Evolution-of-Todo-app/phase-2/backend/app/database.py"
tests_yaml: []
---

# Fix Database Connection Issue in Backend

## Problem
The FastAPI backend was failing to start with a database connection error:
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

## Root Cause
The application was not properly loading the DATABASE_URL from the .env file. The database.py file had a hardcoded placeholder URL instead of using the environment variable.

## Solution
Added `load_dotenv()` import and call to the database.py file to properly load environment variables from the .env file.

## Files Modified
- `/mnt/f/The-Evolution-of-Todo-app/phase-2/backend/app/database.py`: Added `from dotenv import load_dotenv` and `load_dotenv()` call

## Outcome
Backend now successfully connects to the Neon PostgreSQL database specified in the .env file and starts without errors on port 8001.

## Evaluation
- Fixed database connection issue
- Backend starts successfully
- Properly loads environment variables from .env file