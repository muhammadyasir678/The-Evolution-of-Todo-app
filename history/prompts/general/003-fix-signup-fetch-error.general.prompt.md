---
id: "003"
title: "Fix Signup Fetch Error in Frontend"
stage: "general"
date_iso: "2026-01-29"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "001-full-stack-auth"
user: "user"
command: "fix-signup-error"
labels: ["authentication", "bcrypt", "security", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "/mnt/f/The-Evolution-of-Todo-app/phase-2/backend/app/routes/auth.py"
tests_yaml: []
---

# Fix Signup Fetch Error in Frontend

## Problem
The frontend was showing "Failed to fetch" error when attempting to sign up users. The backend was returning a 500 Internal Server Error when the signup endpoint was called.

## Root Cause
The issue was caused by bcrypt compatibility problems with the passlib library. The bcrypt module had version compatibility issues causing AttributeError when trying to access __about__.__version__, and bcrypt has a 72-byte password length limitation.

## Solution
Updated the password hashing scheme from bcrypt to pbkdf2_sha256 in the auth.py file to avoid the compatibility issues.

## Files Modified
- `/mnt/f/The-Evolution-of-Todo-app/phase-2/backend/app/routes/auth.py`: Changed password hashing scheme from bcrypt to pbkdf2_sha256

## Outcome
- Signup endpoint now works correctly
- Signin endpoint also works correctly
- Both authentication flows return proper JWT tokens
- Frontend should now be able to successfully register and authenticate users

## Evaluation
- Signup endpoint tested and returns proper response with user data and token
- Signin endpoint tested and returns proper response with user data and token
- No more "Failed to fetch" errors
- Authentication system functional