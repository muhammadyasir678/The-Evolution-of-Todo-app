# Data Model: Advanced Cloud Deployment

**Feature**: Advanced Cloud Deployment (Phase V)
**Date**: 2026-02-05
**Branch**: 002-advanced-cloud-deployment

## Overview

This document describes the extended data models for the Advanced Cloud Deployment feature, building upon the existing Phase III data models with new fields and entities to support recurring tasks, due date reminders, priority management, and event-driven architecture.

## Extended Task Entity

The Task entity is extended from Phase III to include advanced features:

### Task
- **id**: Integer (Primary Key, Auto-generated)
- **user_id**: String (Foreign Key reference to user)
- **title**: String (Required, max 255 characters)
- **description**: Text (Optional, nullable)
- **completed**: Boolean (Default: false)
- **created_at**: DateTime (Auto-generated, UTC)
- **updated_at**: DateTime (Auto-generated, updates on change, UTC)
- **priority**: Enum ("high", "medium", "low") (Default: "medium", Nullable)
- **tags**: Array of Strings (Optional, stored as JSONB)
- **due_date**: DateTime (Nullable, stores date and time in UTC)
- **reminder_time**: DateTime (Nullable, stores time offset from due_date in seconds)
- **recurrence_pattern**: String (Enum: "daily", "weekly", "monthly", nullable)
- **recurrence_interval**: Integer (Nullable, e.g., every 2 weeks)
- **parent_task_id**: Integer (Foreign Key reference to parent task, nullable, for recurring tasks)

### Validation Rules
- **Title**: Required, max 255 characters, cannot be empty
- **Priority**: Must be one of "high", "medium", "low" if provided
- **Tags**: Maximum 10 tags per task, each tag max 50 characters
- **Due Date**: Cannot be in the past when setting reminder
- **Recurrence**: Pattern and interval must be valid together
- **Parent Task**: Must reference an existing task if provided

### State Transitions
- **Created**: Task is initially created with completed = false
- **Updated**: Task details changed, updated_at timestamp updated
- **Completed**: Task marked as completed, triggers recurring logic if applicable
- **Deleted**: Task removed (soft delete with deleted_at field)

## New AuditLog Entity

### AuditLog
- **id**: Integer (Primary Key, Auto-generated)
- **user_id**: String (Reference to user)
- **task_id**: Integer (Reference to task)
- **action**: String (Enum: "created", "updated", "deleted", "completed")
- **details**: JSONB (Contains full task object or specific changes)
- **timestamp**: DateTime (Auto-generated, UTC)
- **correlation_id**: String (For tracking related events in event flows)

### Validation Rules
- **Action**: Must be one of the allowed enum values
- **Details**: Must be valid JSON format
- **Timestamp**: Auto-populated on creation

## Event Models

### TaskEvent
```json
{
  "event_id": "uuid-string",
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "user_id": "user_abc",
  "task_data": {
    "id": 123,
    "user_id": "user_abc",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-18T10:30:00Z",
    "updated_at": "2026-01-18T10:30:00Z",
    "priority": "high",
    "tags": ["work", "important"],
    "due_date": "2026-01-19T17:00:00Z",
    "reminder_time": "2026-01-19T16:00:00Z",
    "recurrence_pattern": "weekly",
    "recurrence_interval": 1,
    "parent_task_id": null
  },
  "timestamp": "2026-01-18T10:30:00Z",
  "correlation_id": "uuid-string",
  "source_service": "backend-api"
}
```

### ReminderEvent
```json
{
  "event_id": "uuid-string",
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Submit report",
  "due_at": "2026-01-19T17:00:00Z",
  "remind_at": "2026-01-19T16:00:00Z",
  "notification_preferences": {
    "email": true,
    "browser_push": true
  },
  "timestamp": "2026-01-18T10:30:00Z",
  "correlation_id": "uuid-string"
}
```

### TaskUpdateEvent
```json
{
  "event_id": "uuid-string",
  "user_id": "user_abc",
  "task_id": 123,
  "action": "created|updated|completed|deleted",
  "task_data": {
    "id": 123,
    "title": "Task title",
    "completed": false,
    "priority": "high",
    "due_date": "2026-01-19T17:00:00Z"
  },
  "timestamp": "2026-01-18T10:30:00Z",
  "correlation_id": "uuid-string",
  "source_service": "backend-api"
}
```

## Relationship Diagram

```
Users (One-to-Many) <- Task -> (One-to-Many) Child Recurring Tasks
     |                      |
     |                      +-> (One-to-Many) AuditLog
     |
     +-> (One-to-Many) Tasks
```

## Database Indexes

### Primary Indexes
- `idx_tasks_user_id`: For efficient user-specific queries
- `idx_tasks_due_date`: For efficient due date filtering
- `idx_tasks_completed`: For filtering completed tasks
- `idx_audit_log_task_id`: For audit trail lookup by task

### Composite Indexes
- `idx_tasks_priority_completed`: For priority-based filtering with completion status
- `idx_tasks_user_priority`: For user-specific priority queries
- `idx_tasks_tags_gin`: GIN index for efficient array(tag) queries
- `idx_audit_log_user_action_time`: For user audit trail with action and time

### Performance Optimizations
- Partial indexes for frequently queried subsets (e.g., incomplete tasks)
- Covering indexes for common query patterns
- Time-series partitioning for audit logs

## API Contract Models

### Request/Response Models

#### Create Task Request
```json
{
  "title": "Task title",
  "description": "Task description",
  "priority": "high",
  "tags": ["work", "important"],
  "due_date": "2026-01-19T17:00:00Z",
  "reminder_time": 3600,  // seconds before due date
  "recurrence_pattern": "weekly",
  "recurrence_interval": 1
}
```

#### Task Response
```json
{
  "id": 123,
  "user_id": "user_abc",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-18T10:30:00Z",
  "updated_at": "2026-01-18T10:30:00Z",
  "priority": "high",
  "tags": ["work", "important"],
  "due_date": "2026-01-19T17:00:00Z",
  "reminder_time": "2026-01-19T16:00:00Z",
  "recurrence_pattern": "weekly",
  "recurrence_interval": 1,
  "parent_task_id": null
}
```

#### Filter Request Parameters
- `priority`: high|medium|low (optional, multiple allowed)
- `tags`: Comma-separated list of tags (optional, multiple allowed)
- `due_after`: ISO date string (optional)
- `due_before`: ISO date string (optional)
- `status`: completed|pending|all (default: all)
- `sort_by`: due_date|priority|created_date|title (default: created_date)
- `sort_order`: asc|desc (default: desc)

## Constraints and Business Rules

### Task Creation Constraints
- Users can only create tasks for their own user_id
- Recurrence pattern must be valid when recurrence_interval is provided
- Reminder time must be before due date
- Maximum 1000 tasks per user (to prevent performance issues)

### Task Update Constraints
- Completed tasks with recurrence pattern generate next occurrence
- Due date updates may trigger reminder rescheduling
- Parent tasks cannot be modified while child recurrences exist

### Task Deletion Constraints
- Child recurring tasks are soft-deleted (marked as cancelled)
- Parent tasks cannot be deleted if active recurrences exist
- Audit trail preserved for compliance

## Migration Considerations

### From Phase III
- Add new columns to existing tasks table
- Backfill default values for existing records
- Create new audit_log table
- Update foreign key constraints appropriately

### Column Specifications
- `priority`: VARCHAR(10) DEFAULT 'medium', CHECK constraint for allowed values
- `tags`: JSONB[] array with maximum length validation
- `due_date`: TIMESTAMP with timezone, nullable
- `reminder_time`: INTERVAL or INTEGER representing seconds, nullable
- `recurrence_pattern`: VARCHAR(10) with CHECK constraint, nullable
- `recurrence_interval`: INTEGER with positive value constraint, nullable
- `parent_task_id`: INTEGER with foreign key reference, nullable

## Performance Benchmarks

### Expected Query Performance
- Task retrieval by user: <50ms (with proper indexing)
- Filtered task queries: <100ms (with composite indexes)
- Tag-based searches: <200ms (with GIN indexes)
- Recurrence calculation: <50ms (with efficient date libraries)
- Event publishing: <10ms (with async Kafka producers)

### Scalability Targets
- Support 10,000+ tasks per user
- Handle 1,000+ concurrent users
- Process 100+ events per second
- Maintain <200ms p95 response time