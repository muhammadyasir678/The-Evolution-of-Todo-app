'use client';

import React, { useEffect, useState, useRef } from 'react';
import TaskItem from './TaskItem';
import TaskDueDate from './TaskDueDate';
import TaskFilters from './TaskFilters';
import TaskPriority from './TaskPriority';
import TaskRecurrence from './TaskRecurrence';
import TaskSearch from './TaskSearch';
import TaskTags from './TaskTags';
import { Task } from '../lib/types';
import { taskApi } from '../lib/api';
import WebSocketService from '../lib/websocketService';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const webSocketService = useRef<WebSocketService>(WebSocketService.getInstance());

  // Fetch tasks when component mounts or when userId changes
  useEffect(() => {
    fetchTasks();
    
    // Connect to WebSocket for real-time updates
    webSocketService.current.connect(userId);
    
    // Subscribe to WebSocket events
    const unsubscribe = webSocketService.current.subscribe(handleWebSocketEvent);
    
    // Cleanup on unmount
    return () => {
      unsubscribe();
    };
  }, [userId]);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await taskApi.getTasks(userId);
      if (result.error) {
        setError(result.error);
      } else {
        setTasks(result.data || []);
      }
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Task fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleWebSocketEvent = (event: any) => {
    console.log('Handling WebSocket event:', event);
    const { action, task_data, task_id } = event;
    
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
    // With WebSocket, we don't need to fetch tasks anymore since updates come in real-time
    // But we'll keep this for backward compatibility with components that still call it
  };

  const handleTaskDeleted = () => {
    // With WebSocket, we don't need to fetch tasks anymore since deletes come in real-time
    // But we'll keep this for backward compatibility with components that still call it
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

  if (tasks.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="text-center py-8">
          <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
          <p className="text-gray-500">Create your first task using the form above!</p>
          <div className="mt-2 text-xs text-gray-500">
            WebSocket Status: {webSocketService.current.getConnectionStatus()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">Your Tasks ({tasks.length})</h2>
      <div className="text-xs text-gray-500 mb-2">
        WebSocket Status: {webSocketService.current.getConnectionStatus()}
      </div>

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
    </div>
  );
};

export default TaskList;