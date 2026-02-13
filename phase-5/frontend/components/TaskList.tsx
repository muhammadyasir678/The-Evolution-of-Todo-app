'use client';

import React, { useState, useEffect } from 'react';
import { Task } from '../lib/types';
import { taskApi } from '../lib/api';
import TaskFilters from './TaskFilters';
import TaskSearch from './TaskSearch';
import WebSocketService from '../lib/websocketService';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filter and sort states
  const [filters, setFilters] = useState({
    priority: '',
    tags: '',
    status: 'all',
    dueAfter: '',
    dueBefore: ''
  });
  
  const [sortConfig, setSortConfig] = useState({
    sortBy: 'created_at',
    sortOrder: 'desc'
  });
  
  const [searchQuery, setSearchQuery] = useState('');

  const webSocketService = WebSocketService.getInstance();

  // Load sort preferences from localStorage
  useEffect(() => {
    const savedSort = localStorage.getItem('taskSortConfig');
    if (savedSort) {
      try {
        const parsed = JSON.parse(savedSort);
        setSortConfig(parsed);
      } catch (e) {
        console.error('Error parsing sort config from localStorage', e);
      }
    }
  }, []);

  // Save sort preferences to localStorage
  const saveSortConfig = (config: { sortBy: string; sortOrder: string }) => {
    localStorage.setItem('taskSortConfig', JSON.stringify(config));
  };

  // Fetch tasks with filters and sorting
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
      
      const result = await taskApi.getTasks(
        userId,
        filters.priority,
        tagsFilter,
        filters.status,
        filters.dueAfter,
        filters.dueBefore,
        sortConfig.sortBy,
        sortConfig.sortOrder
      );
      
      if (result.error) {
        setError(result.error);
      } else {
        setTasks(result.data || []);
      }
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Task fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle filter changes
  const handleFilterChange = (filterName: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  // Handle sort change
  const handleSortChange = (sortBy: string, sortOrder: string) => {
    const newConfig = { sortBy, sortOrder };
    setSortConfig(newConfig);
    saveSortConfig(newConfig);
  };

  // Handle search
  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  // Refresh tasks when filters or sort change
  useEffect(() => {
    fetchTasks();
  }, [filters, sortConfig, searchQuery]);

  // Set up WebSocket listener for real-time updates
  useEffect(() => {
    const handleTaskUpdate = (data: any) => {
      // Refresh the task list when a task is updated
      fetchTasks();
    };

    webSocketService.addMessageHandler('task_update', handleTaskUpdate);
    
    // Cleanup function
    return () => {
      webSocketService.removeMessageHandler('task_update', handleTaskUpdate);
    };
  }, [userId]);

  const toggleTaskCompletion = async (task: Task) => {
    try {
      const result = await taskApi.toggleTaskCompletion(
        userId,
        task.id,
        !task.completed
      );
      
      if (result.error) {
        setError(result.error);
      } else {
        // The WebSocket handler will refresh the list automatically
      }
    } catch (err) {
      setError('Failed to update task');
      console.error('Task update error:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
        {error}
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">Your Tasks</h2>
      
      {/* Search and Filters */}
      <div className="mb-6 space-y-4">
        <TaskSearch onSearch={handleSearch} />
        <TaskFilters 
          filters={filters}
          onFilterChange={handleFilterChange}
          onSortChange={handleSortChange}
          currentSort={sortConfig}
        />
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No tasks found</p>
      ) : (
        <div className="space-y-3">
          {tasks.map(task => (
            <div 
              key={task.id} 
              className={`p-4 border rounded-md ${
                task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleTaskCompletion(task)}
                    className="mt-1 h-4 w-4 text-indigo-600 rounded focus:ring-indigo-500"
                  />
                  <div>
                    <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                        {task.description}
                      </p>
                    )}
                    
                    {/* Task metadata */}
                    <div className="mt-2 flex flex-wrap gap-2 text-xs">
                      {task.priority && (
                        <span className={`px-2 py-1 rounded-full ${
                          task.priority === 'high' ? 'bg-red-100 text-red-800' :
                          task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                        </span>
                      )}
                      
                      {task.tags && task.tags.split(',').map((tag, idx) => (
                        <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                          {tag.trim()}
                        </span>
                      ))}
                      
                      {task.due_date && (
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full">
                          Due: {new Date(task.due_date).toLocaleDateString()}
                        </span>
                      )}
                      
                      {task.recurrence_pattern && (
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded-full">
                          Repeats: {task.recurrence_pattern}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="text-xs text-gray-500">
                  {new Date(task.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;