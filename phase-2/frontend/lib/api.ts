import { Task, CreateTaskRequest, UpdateTaskRequest, ApiResponse } from './types';
import { useSession } from './auth';

// Base API URL from environment
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://muhammadyasir786-backend.hf.space';

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    // Get the auth token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth-token') : null;

    const url = `${BASE_URL}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        error: errorData.detail || `HTTP error! status: ${response.status}`,
        message: errorData.message || 'Request failed',
      };
    }

    const data = await response.json();
    return { data };
  } catch (error: any) {
    return {
      error: error.message || 'Network error occurred',
      message: 'Failed to communicate with server',
    };
  }
}

// Task API functions
export const taskApi = {
  // Get all tasks for a user
  getTasks: async (userId: string): Promise<ApiResponse<Task[]>> => {
    return apiRequest<Task[]>(`/api/${userId}/tasks`);
  },

  // Create a new task
  createTask: async (
    userId: string,
    taskData: CreateTaskRequest
  ): Promise<ApiResponse<Task>> => {
    return apiRequest<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  // Get a specific task
  getTask: async (userId: string, taskId: number): Promise<ApiResponse<Task>> => {
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`);
  },

  // Update a task
  updateTask: async (
    userId: string,
    taskId: number,
    taskData: UpdateTaskRequest
  ): Promise<ApiResponse<Task>> => {
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: number): Promise<ApiResponse<void>> => {
    return apiRequest<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },

  // Toggle task completion
  toggleTaskCompletion: async (
    userId: string,
    taskId: number,
    completed: boolean
  ): Promise<ApiResponse<Task>> => {
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  },
};

// Export the API functions
export default taskApi;