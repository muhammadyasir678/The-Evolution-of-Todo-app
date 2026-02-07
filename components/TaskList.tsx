'use client';

import React, { useEffect, useState } from 'react';
import TaskItem from './TaskItem';
import { Task } from '../lib/types';
import { taskApi } from '../lib/api';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks when component mounts or when tasks change
  useEffect(() => {
    fetchTasks();
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

  const handleTaskUpdated = () => {
    fetchTasks(); // Refresh the task list
  };

  const handleTaskDeleted = () => {
    fetchTasks(); // Refresh the task list
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
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">Your Tasks ({tasks.length})</h2>

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