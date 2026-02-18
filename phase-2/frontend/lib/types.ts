// TypeScript types for the todo application

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  due_date?: string | null;
  reminder_time?: string | null;
  priority?: string;
  tags?: string;  // Comma-separated string
  recurrence_pattern?: string | null;
  recurrence_interval?: number | null;
  parent_task_id?: number | null;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  name?: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date?: string | null;
  reminder_time?: string | null;
  priority?: string;
  tags?: string;  // Comma-separated string
  recurrence_pattern?: string | null;
  recurrence_interval?: number | null;
  parent_task_id?: number | null;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string | null;
  reminder_time?: string | null;
  priority?: string;
  tags?: string;  // Comma-separated string
  recurrence_pattern?: string | null;
  recurrence_interval?: number | null;
  parent_task_id?: number | null;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}