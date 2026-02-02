# Functional Testing Checklist

This document outlines the tests that have been functionally verified for the Todo application.

## Phase 3: New User Registration and First Task (US1)

### T030: Test complete user flow: sign up → create first task
- [x] User can navigate to homepage and is redirected to sign-in
- [x] User can access sign-up page via sign-in page
- [x] User can register with valid email and password
- [x] User is automatically signed in after successful registration
- [x] User is redirected to tasks page after sign-in
- [x] User sees empty task list initially
- [x] User can create first task with valid title (1-200 chars)
- [x] User can optionally add description (max 1000 chars)
- [x] Created task appears in task list immediately
- [x] Form validation prevents invalid task creation (empty title, too long title/description)

## Phase 4: Returning User Task Management (US2)

### T042: Test complete user flow: sign in → view/update/delete/complete tasks
- [x] User can sign in with registered credentials
- [x] User sees their existing tasks on tasks page
- [x] User can create new tasks
- [x] User can update existing tasks (title and description)
- [x] User can mark tasks as complete/incomplete using checkbox
- [x] User can delete tasks after confirmation
- [x] All operations show appropriate loading states
- [x] All operations show appropriate success/error messages
- [x] All changes are persisted and visible after page refresh

## Phase 5: Multi-user Isolation (US3)

### T046: Test user isolation: User A cannot access User B's tasks
- [x] Backend enforces user_id matching in JWT token and URL
- [x] Attempting to access another user's tasks returns 403 Forbidden
- [x] Database queries are filtered by authenticated user_id
- [x] Each user only sees their own tasks

### T048: Add tests to verify data isolation between users
- [x] Task creation only creates tasks for authenticated user
- [x] Task updates only affect tasks owned by authenticated user
- [x] Task deletion only affects tasks owned by authenticated user
- [x] JWT token validation ensures proper user context

## Phase 6: Polish & Cross-Cutting Concerns

### T052: Optimize API performance and response times
- [x] Database queries use proper indexing on user_id
- [x] API responses are appropriately structured
- [x] Error handling doesn't cause performance issues

### T053: Write backend unit tests for all endpoints
- [x] All API endpoints properly validate user authentication
- [x] All endpoints enforce user-specific data filtering
- [x] Error responses are consistent and informative
- [x] Validation prevents invalid data from being stored

### T058: Test end-to-end functionality in development environment
- [x] Frontend and backend communicate properly via API
- [x] All CRUD operations work end-to-end
- [x] Authentication flow works completely
- [x] User interface responds appropriately to all operations

### T059: Prepare for deployment to production
- [x] Environment variables properly configured
- [x] Security headers implemented
- [x] CORS configured for production domains
- [x] JWT token expiration handling in place
- [x] Input validation and sanitization implemented

## Additional Verifications

- [x] Responsive design works on mobile, tablet, and desktop
- [x] Loading states provide feedback during API operations
- [x] Error messages are user-friendly
- [x] Success notifications confirm completed actions
- [x] Form validation prevents invalid submissions
- [x] Empty state is displayed when no tasks exist
- [x] Completed tasks are visually distinguished
- [x] Sign out functionality works properly