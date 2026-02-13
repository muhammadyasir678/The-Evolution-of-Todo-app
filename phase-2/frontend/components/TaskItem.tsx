'use client';

import React, { useState } from 'react';
import { FiEdit, FiTrash2, FiSave, FiX } from 'react-icons/fi';
import { Task, UpdateTaskRequest } from '../lib/types';
import { taskApi } from '../lib/api';
import WebSocketService from '../lib/websocketService';

interface TaskItemProps {
  task: Task;
  userId: string;
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, userId, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const webSocketService = WebSocketService.getInstance();

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      const result = await taskApi.toggleTaskCompletion(userId, task.id, !task.completed);
      if (!result.error) {
        // The backend will emit a WebSocket event, which will be handled by TaskList
        // We don't need to do anything here as the TaskList component handles WebSocket events
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to update task');
      console.error('Task update error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setTitle(task.title);
    setDescription(task.description || '');
    setError(null);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setTitle(task.title);
    setDescription(task.description || '');
    setError(null);
  };

  const handleSaveEdit = async () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length < 1 || title.length > 200) {
      setError('Title must be between 1 and 200 characters');
      return;
    }

    if (description && description.length > 1000) {
      setError('Description must be less than 1000 characters');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const updateData: UpdateTaskRequest = {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      const result = await taskApi.updateTask(userId, task.id, updateData);
      if (!result.error) {
        setIsEditing(false);
        // The backend will emit a WebSocket event, which will be handled by TaskList
        // We don't need to do anything here as the TaskList component handles WebSocket events
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to update task');
      console.error('Task update error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete the task "${task.title}"?`)) {
      setLoading(true);
      try {
        const result = await taskApi.deleteTask(userId, task.id);
        if (!result.error) {
          // The backend will emit a WebSocket event, which will be handled by TaskList
          // We don't need to do anything here as the TaskList component handles WebSocket events
        } else {
          setError(result.error);
        }
      } catch (err) {
        setError('Failed to delete task');
        console.error('Task deletion error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 ${task.completed ? 'bg-green-50' : 'bg-white'} shadow-sm`}>
      {error && (
        <div className="mb-2 p-2 bg-red-100 text-red-700 rounded text-sm">
          {error}
        </div>
      )}

      {isEditing ? (
        // Edit mode
        <div>
          <div className="mb-2">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-2"
              disabled={loading}
              maxLength={200}
            />
          </div>

          <div className="mb-3">
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={2}
              disabled={loading}
              maxLength={1000}
            />
          </div>

          <div className="flex space-x-2">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className={`flex items-center px-3 py-1 rounded text-white text-sm ${
                loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              <FiSave className="mr-1" /> Save
            </button>

            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className={`flex items-center px-3 py-1 rounded text-white text-sm ${
                loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gray-500 hover:bg-gray-600'
              }`}
            >
              <FiX className="mr-1" /> Cancel
            </button>
          </div>
        </div>
      ) : (
        // Display mode
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              disabled={loading}
              className="mt-1 mr-3 h-5 w-5 rounded text-indigo-600 focus:ring-indigo-500"
            />

            <div className="flex-1">
              <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h3>

              {task.description && (
                <p className={`mt-1 text-gray-600 ${task.completed ? 'line-through' : ''}`}>
                  {task.description}
                </p>
              )}

              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && (
                  <span>, Updated: {new Date(task.updated_at).toLocaleString()}</span>
                )}
              </div>
            </div>

            <div className="flex space-x-2 ml-2">
              <button
                onClick={handleEdit}
                disabled={loading}
                className={`p-2 rounded-full ${
                  loading ? 'text-gray-400 cursor-not-allowed' : 'text-blue-600 hover:bg-blue-100'
                }`}
                title="Edit task"
              >
                <FiEdit />
              </button>

              <button
                onClick={handleDelete}
                disabled={loading}
                className={`p-2 rounded-full ${
                  loading ? 'text-gray-400 cursor-not-allowed' : 'text-red-600 hover:bg-red-100'
                }`}
                title="Delete task"
              >
                <FiTrash2 />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;