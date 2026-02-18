'use client';

import React, { useState } from 'react';
import { FiEdit, FiTrash2, FiSave, FiX } from 'react-icons/fi';
import { Task, UpdateTaskRequest } from '../lib/types';
import { taskApi } from '../lib/api';
import WebSocketService from '../lib/websocketService';
import TaskDueDate from './TaskDueDate';
import TaskPriority from './TaskPriority';
import TaskRecurrence from './TaskRecurrence';
import TaskTags from './TaskTags';

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
  const [dueDate, setDueDate] = useState<string | null>(task.due_date ?? null);
  const [reminderTime, setReminderTime] = useState<string | null>(task.reminder_time ?? null);
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>(task.priority as 'high' | 'medium' | 'low' || 'medium');
  const [tags, setTags] = useState<string>(task.tags || '');
  const [recurrencePattern, setRecurrencePattern] = useState<string>(task.recurrence_pattern || '');
  const [recurrenceInterval, setRecurrenceInterval] = useState<number>(task.recurrence_interval || 1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const webSocketService = WebSocketService.getInstance();

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      const result = await taskApi.toggleTaskCompletion(userId, task.id, !task.completed);
      if (!result.error) {
        // Since WebSocket is disabled, manually trigger a refresh
        onTaskUpdated();
      } else {
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
          setError('An unknown error occurred while updating the task');
        }
      }
    } catch (err: any) {
      // Handle both string and object errors
      if (typeof err === 'string') {
        setError(err);
      } else if (typeof err === 'object' && err !== null && err.hasOwnProperty('message')) {
        setError(err.message as string);
      } else {
        setError('Failed to update task');
      }
      console.error('Task update error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setTitle(task.title);
    setDescription(task.description || '');
    setDueDate(task.due_date ?? null);
    setReminderTime(task.reminder_time ?? null);
    setPriority(task.priority as 'high' | 'medium' | 'low' || 'medium');
    setTags(task.tags || '');
    setRecurrencePattern(task.recurrence_pattern || '');
    setRecurrenceInterval(task.recurrence_interval || 1);
    setError(null);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setTitle(task.title);
    setDescription(task.description || '');
    setDueDate(task.due_date ?? null);
    setReminderTime(task.reminder_time ?? null);
    setPriority(task.priority as 'high' | 'medium' | 'low' || 'medium');
    setTags(task.tags || '');
    setRecurrencePattern(task.recurrence_pattern || '');
    setRecurrenceInterval(task.recurrence_interval || 1);
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
        due_date: dueDate,
        reminder_time: reminderTime,
        priority: priority,
        tags: tags || undefined,
        recurrence_pattern: recurrencePattern || undefined,
        recurrence_interval: recurrenceInterval || undefined,
      };

      const result = await taskApi.updateTask(userId, task.id, updateData);
      if (!result.error) {
        setIsEditing(false);
        // Since WebSocket is disabled, manually trigger a refresh
        onTaskUpdated();
      } else {
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
          setError('An unknown error occurred while updating the task');
        }
      }
    } catch (err: any) {
      // Handle both string and object errors
      if (typeof err === 'string') {
        setError(err);
      } else if (typeof err === 'object' && err !== null && err.hasOwnProperty('message')) {
        setError(err.message as string);
      } else {
        setError('Failed to update task');
      }
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
          // Since WebSocket is disabled, manually trigger a refresh
          onTaskDeleted();
        } else {
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
            setError('An unknown error occurred while deleting the task');
          }
        }
      } catch (err: any) {
        // Handle both string and object errors
        if (typeof err === 'string') {
          setError(err);
        } else if (typeof err === 'object' && err !== null && 'message' in err) {
          setError(err.message as string);
        } else {
          setError('Failed to delete task');
        }
        console.error('Task deletion error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  // Format date for display
  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString();
  };

  // Render priority badge
  const renderPriorityBadge = (priority: string) => {
    const priorityClasses = {
      low: 'bg-blue-100 text-blue-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-red-100 text-red-800',
    };
    
    const priorityLabel = priority.charAt(0).toUpperCase() + priority.slice(1);
    
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${priorityClasses[priority as keyof typeof priorityClasses] || priorityClasses.medium}`}>
        {priorityLabel}
      </span>
    );
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

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <TaskDueDate
                dueDate={dueDate}
                reminderTime={reminderTime}
                onDueDateChange={setDueDate}
                onReminderChange={setReminderTime}
              />
            </div>

            <div className="space-y-4">
              <TaskPriority priority={priority} setPriority={setPriority} />

              <TaskTags tags={tags} onChange={setTags} />

              <TaskRecurrence
                recurrencePattern={recurrencePattern}
                recurrenceInterval={recurrenceInterval}
                onPatternChange={setRecurrencePattern}
                onIntervalChange={setRecurrenceInterval}
              />
            </div>
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
              <div className="flex items-center justify-between">
                <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                  {task.title}
                </h3>
                
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

              {task.description && (
                <p className={`mt-1 text-gray-600 ${task.completed ? 'line-through' : ''}`}>
                  {task.description}
                </p>
              )}

              {/* Additional task properties */}
              <div className="mt-3 space-y-2">
                {task.due_date && (
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="font-medium">Due:</span>
                    <span className="ml-2">{formatDate(task.due_date)}</span>
                  </div>
                )}

                {task.reminder_time && (
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="font-medium">Reminder:</span>
                    <span className="ml-2">{formatDate(task.reminder_time)}</span>
                  </div>
                )}

                {task.priority && (
                  <div className="flex items-center">
                    <span className="font-medium text-sm text-gray-600 mr-2">Priority:</span>
                    {renderPriorityBadge(task.priority)}
                  </div>
                )}

                {task.tags && (
                  <div className="flex flex-wrap gap-1">
                    {task.tags.split(',').map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                      >
                        {tag.trim()}
                      </span>
                    ))}
                  </div>
                )}

                {task.recurrence_pattern && (
                  <div className="flex items-center text-sm text-gray-600">
                    <span className="font-medium">Repeats:</span>
                    <span className="ml-2 capitalize">
                      {task.recurrence_pattern} every {task.recurrence_interval} {task.recurrence_pattern === 'daily' ? 'day(s)' : task.recurrence_pattern === 'weekly' ? 'week(s)' : 'month(s)'}
                    </span>
                  </div>
                )}
              </div>

              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && (
                  <span>, Updated: {new Date(task.updated_at).toLocaleString()}</span>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;