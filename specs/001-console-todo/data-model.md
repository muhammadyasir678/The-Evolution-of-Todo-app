# Data Model: Phase I - In-Memory Python Console App

## Task Entity

### Attributes
- **id**: int (auto-incrementing unique identifier)
  - Type: Positive integer
  - Required: Yes
  - Constraints: Must be unique, auto-generated

- **title**: str (required task title)
  - Type: String
  - Required: Yes
  - Constraints: 1-200 characters, cannot be empty or whitespace only

- **description**: str (optional task description)
  - Type: String
  - Required: No
  - Constraints: Max 1000 characters, can be empty

- **completed**: bool (completion status)
  - Type: Boolean
  - Required: Yes
  - Default: False
  - Constraints: True (completed) or False (incomplete)

- **created_at**: datetime (timestamp of creation)
  - Type: datetime object
  - Required: Yes
  - Default: Current timestamp at creation
  - Constraints: Immutable after creation

### Validation Rules
1. Title validation:
   - Length: 1-200 characters
   - Cannot be empty or contain only whitespace
   - Trimmed of leading/trailing whitespace

2. Description validation:
   - Length: 0-1000 characters
   - Optional field, can be empty

3. ID validation:
   - Must be positive integer
   - Must be unique within the system
   - Auto-generated using internal counter

### State Transitions
- **Initial State**: completed = False (upon creation)
- **Transition 1**: completed = False → completed = True (when marked complete)
- **Transition 2**: completed = True → completed = False (when marked incomplete)

## Task Collection (In-Memory Storage)

### Structure
- **Type**: Dictionary mapping (dict[int, Task])
- **Key**: Task.id (integer)
- **Value**: Task object
- **Access**: O(1) lookup by ID

### Operations
1. **Add Task**: Insert new Task object with auto-generated ID
2. **Get Task**: Retrieve Task by ID
3. **Update Task**: Modify existing Task properties (except ID)
4. **Delete Task**: Remove Task by ID
5. **List Tasks**: Retrieve all Task objects

### Internal Counter
- **next_id**: Integer counter for auto-incrementing IDs
- **Initial Value**: 1
- **Increment Rule**: Increase by 1 for each new task
- **Persistence**: Exists only in memory during application runtime