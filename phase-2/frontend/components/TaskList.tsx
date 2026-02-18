'use client';

import React, { useEffect, useState, useRef } from 'react';
import TaskItem from './TaskItem';
import TaskFilters from './TaskFilters';
import TaskSearch from './TaskSearch';
import { Task } from '../lib/types';
import { taskApi } from '../lib/api';
import WebSocketService from '../lib/websocketService';

interface FilterOptions {
  priority?: string;
  tags?: string;
  status?: string;
  dueDateRange?: { start?: string; end?: string };
}

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<FilterOptions>({});
  const [sortConfig, setSortConfig] = useState({
    sortBy: 'created_at',
    sortOrder: 'desc'
  });
  const webSocketService = useRef<WebSocketService>(WebSocketService.getInstance());

  // Fetch tasks when component mounts or when userId changes
  useEffect(() => {
    fetchTasks();

    // Try to connect to WebSocket for real-time updates (will be disabled)
    webSocketService.current.connect(userId);

    // Subscribe to WebSocket events (won't receive any since WS is disabled)
    const unsubscribe = webSocketService.current.subscribe(handleWebSocketEvent);

    // Setup polling since WebSocket is disabled
    const pollInterval = setInterval(() => {
      console.log("Polling for task updates...");
      fetchTasks();
    }, 30000); // 30 seconds

    // Cleanup on unmount
    return () => {
      unsubscribe();
      clearInterval(pollInterval);
    };
  }, [userId, filters, searchQuery, sortConfig]);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      // Apply search filter to tags if search query exists
      let tagsFilter = filters.tags;
      if (searchQuery) {
        // If search query exists, treat it as additional tags filter
        tagsFilter = tagsFilter ? `${tagsFilter},${searchQuery}` : searchQuery;
      }

      const result = await taskApi.getFilteredTasks(
        userId,
        filters.priority,
        tagsFilter,
        filters.status,
        filters.dueDateRange?.start,
        filters.dueDateRange?.end,
        sortConfig.sortBy,
        sortConfig.sortOrder
      );

      if (result.error) {
        // Handle both string and object errors
        if (typeof result.error === 'string') {
          setError(result.error);
        } else if (typeof result.error === 'object' && result.error !== null) {
          // If it's an object, try to extract a meaningful message
          if ('message' in result.error) {
            setError((result.error as any).message as string);
          } else if ('detail' in result.error) {
            setError((result.error as any).detail as string);
          } else {
            setError(JSON.stringify(result.error));
          }
        } else {
          setError('An unknown error occurred while fetching tasks');
        }
      } else {
        setTasks(result.data || []);
      }
    } catch (err: any) {
      // Handle both string and object errors
      if (typeof err === 'string') {
        setError(err);
      } else if (typeof err === 'object' && err !== null && 'message' in err) {
        setError(err.message as string);
      } else {
        setError('Failed to load tasks');
      }
      console.error('Task fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleWebSocketEvent = (event: any) => {
    console.log('Handling WebSocket event:', event);
    const { action, task_data, task_id, user_id } = event;

    // Only process events for the current user
    if (user_id !== userId) {
      return;
    }

    setTasks(prevTasks => {
      let updatedTasks = [...prevTasks];

      switch (action) {
        case 'create':
          // Add new task if it doesn't already exist
          if (!updatedTasks.some(t => t.id === task_id)) {
            updatedTasks = [...updatedTasks, task_data];
          }
          break;

        case 'update':
          // Update existing task
          updatedTasks = updatedTasks.map(task =>
            task.id === task_id ? { ...task, ...task_data } : task
          );
          break;

        case 'delete':
          // Remove task
          updatedTasks = updatedTasks.filter(task => task.id !== task_id);
          break;

        default:
          console.warn(`Unknown action: ${action}`);
      }

      return updatedTasks;
    });
  };

  const handleTaskUpdated = () => {
    // Since WebSocket is disabled, we need to fetch tasks to update the list
    fetchTasks();
  };

  const handleTaskDeleted = () => {
    // Since WebSocket is disabled, we need to fetch tasks to update the list
    fetchTasks();
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleFilterChange = (newFilters: FilterOptions) => {
    setFilters(newFilters);
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-gray-100 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="p-4 bg-red-100 text-red-700 rounded-md">
          Error: {error}
          <div className="mt-2 text-xs text-red-600">
            WebSocket Status: {webSocketService.current.getConnectionStatus()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <h2 className="text-lg font-semibold text-gray-800">Your Tasks ({tasks.length})</h2>

        <div className="flex flex-col sm:flex-row gap-3">
          <TaskSearch onSearch={handleSearch} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <TaskFilters filters={filters} onFilterChange={handleFilterChange} />
        </div>

        <div className="lg:col-span-3">
          <div className="text-xs text-gray-500 mb-2">
            WebSocket Status: {webSocketService.current.getConnectionStatus()}
            {webSocketService.current.getConnectionStatus() !== 'connected' && (
              <span className="ml-2 text-orange-500">
                {webSocketService.current.getConnectionStatus() === 'disabled' 
                  ? '(Real-time updates disabled)' 
                  : '(Limited real-time updates)'}
              </span>
            )}
          </div>

          {tasks.length === 0 ? (
            <div className="text-center py-8">
              <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks found</h3>
              <p className="text-gray-500">
                {tasks.length === 0
                  ? 'Create your first task using the form above!'
                  : 'Try adjusting your search or filters.'}
              </p>
            </div>
          ) : (
            <div>
              {tasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  userId={userId}
                  onTaskUpdated={handleTaskUpdated}
                  onTaskDeleted={handleTaskDeleted}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskList;