# Demo Video Script: Advanced Cloud Deployment Features

## Introduction (0:00-0:15)
- Welcome to the demo of Phase V: Advanced Cloud Deployment
- Today we'll showcase the new advanced features: recurring tasks, due date reminders, priority management, tagging, and real-time sync

## Feature 1: Recurring Tasks (0:15-1:30)
- Show creating a "Weekly Team Meeting" task
- Set recurrence pattern to "weekly"
- Complete the task
- Demonstrate the system automatically creating the next occurrence
- Highlight the recurrence pattern logic (daily, weekly, monthly)

## Feature 2: Due Date Reminders (1:30-2:45)
- Create a task with a due date (e.g., "Submit quarterly report")
- Set a reminder for 1 hour before the due date
- Show the reminder being scheduled in the system
- Demonstrate the notification being sent (simulated)

## Feature 3: Priority Management (2:45-3:30)
- Create tasks with different priorities (high, medium, low)
- Show the visual indicators for each priority level
- Demonstrate filtering tasks by priority

## Feature 4: Tagging System (3:30-4:15)
- Add tags to tasks (e.g., "work", "personal", "urgent")
- Show the tag management UI
- Demonstrate filtering tasks by tags

## Feature 5: Advanced Filtering and Sorting (4:15-5:00)
- Apply multiple filters (priority, tags, status, due date range)
- Sort tasks by different criteria (due date, priority, created date, title)
- Show how filters and sorts can be combined

## Feature 6: Real-Time Synchronization (5:00-6:00)
- Open the application in multiple browser windows/tabs
- Create a task in one window
- Show it appearing in real-time in other windows
- Update a task in one window and see it update in others
- Demonstrate the WebSocket service broadcasting changes

## Feature 7: Event-Driven Architecture (6:00-7:00)
- Explain the Kafka topics: task-events, reminders, task-updates
- Show how events flow between services
- Demonstrate the Audit Service logging all operations
- Highlight the decoupled nature of the architecture

## Feature 8: Dapr Integration (7:00-7:45)
- Explain how Dapr handles pub/sub for Kafka
- Show Dapr sidecar annotations in Kubernetes deployments
- Highlight the standardized microservices patterns

## Cloud Deployment Overview (7:45-8:30)
- Brief overview of the cloud deployment process
- Mention the CI/CD pipeline
- Show the application running in a cloud environment

## Conclusion (8:30-9:00)
- Recap of all advanced features
- Benefits of the event-driven architecture
- Thank viewers for watching the demo

## Technical Notes for Video Production:
- Use screen recording software to capture the UI interactions
- Narrate each step clearly
- Highlight important elements with cursor effects
- Show both the frontend UI and relevant backend logs/console output
- Use split-screen views when demonstrating real-time sync across multiple windows
- Include diagrams to explain the event-driven flow between services