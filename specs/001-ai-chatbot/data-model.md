# Data Model: AI-Powered Todo Chatbot

## Entity: Conversation

**Description**: Represents a user's chat session with associated metadata

**Fields**:
- id: integer (primary key, auto-increment)
- user_id: string (foreign key -> users.id, indexed for performance)
- created_at: timestamp (automatically set on creation)
- updated_at: timestamp (automatically updated on changes)

**Validation Rules**:
- user_id must exist in users table (referential integrity)
- created_at and updated_at are required and automatically managed
- Each conversation belongs to exactly one user

**State Transitions**: None (immutable conversation record)

## Entity: Message

**Description**: Represents individual chat exchanges with role (user/assistant), content, and timestamp

**Fields**:
- id: integer (primary key, auto-increment)
- user_id: string (foreign key -> users.id, indexed for performance)
- conversation_id: integer (foreign key -> conversations.id, indexed for performance)
- role: string ("user" or "assistant", validated enum)
- content: text (message content, maximum 10,000 characters)
- created_at: timestamp (automatically set on creation)

**Validation Rules**:
- user_id must exist in users table
- conversation_id must exist in conversations table
- role must be either "user" or "assistant"
- content is required and must not exceed 10,000 characters
- created_at is required and automatically managed

**State Transitions**: None (immutable message record)

## Entity: Task (Existing from Phase II)

**Description**: Represents todo items with content, completion status, and user association

**Fields**:
- id: integer (primary key, auto-increment)
- user_id: string (foreign key -> users.id, indexed for performance)
- title: string (task title, maximum 255 characters)
- description: text (optional task description)
- completed: boolean (completion status, default false)
- created_at: timestamp (automatically set on creation)
- updated_at: timestamp (automatically updated on changes)

**Validation Rules**:
- user_id must exist in users table
- title is required and must not exceed 255 characters
- completed defaults to false
- created_at and updated_at are required and automatically managed

**State Transitions**:
- Task moves from incomplete to complete when completed field changes from false to true
- Task remains complete when completed field changes from true to true

## Relationships

**Conversation ↔ Message**:
- One-to-many relationship (one conversation can have many messages)
- Foreign key: Message.conversation_id → Conversation.id
- Cascade delete: When conversation is deleted, all related messages are deleted

**User ↔ Conversation**:
- One-to-many relationship (one user can have many conversations)
- Foreign key: Conversation.user_id → User.id
- No cascade delete: When user is deleted, conversations remain (for audit purposes)

**User ↔ Message**:
- One-to-many relationship (one user can have many messages)
- Foreign key: Message.user_id → User.id
- No cascade delete: When user is deleted, messages remain (for audit purposes)

**User ↔ Task**:
- One-to-many relationship (one user can have many tasks)
- Foreign key: Task.user_id → User.id
- Cascade delete: When user is deleted, all related tasks are deleted

## Indexes

**Required Indexes**:
- conversations.user_id_idx: Index on user_id for fast user lookup
- messages.user_id_idx: Index on user_id for fast user lookup
- messages.conversation_id_idx: Index on conversation_id for fast conversation lookup
- messages.created_at_idx: Index on created_at for chronological ordering
- tasks.user_id_idx: Index on user_id for fast user lookup
- tasks.completed_idx: Index on completed for fast filtering of completed/incomplete tasks

## Constraints

**Data Integrity**:
- Referential integrity enforced for all foreign key relationships
- Unique constraints where applicable
- Check constraints for enum-like fields (role in Message)

**Performance**:
- All frequently queried fields are indexed
- Timestamp fields enable efficient range queries
- Proper indexing for common access patterns (by user, by conversation, by time)

## Access Patterns

**Common Queries**:
1. Retrieve all conversations for a specific user (filtered by user_id)
2. Retrieve all messages for a specific conversation (filtered by conversation_id)
3. Retrieve messages in chronological order (ordered by created_at)
4. Retrieve tasks for a specific user (filtered by user_id)
5. Retrieve completed/incomplete tasks for a specific user (filtered by user_id and completed)