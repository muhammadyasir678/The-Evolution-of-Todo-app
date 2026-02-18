'use client';

import React, { useState } from 'react';
import TaskDueDate from './TaskDueDate';
import TaskPriority from './TaskPriority';
import TaskRecurrence from './TaskRecurrence';
import TaskTags from './TaskTags';
import { CreateTaskRequest } from '../lib/types';
import { taskApi } from '../lib/api';
import WebSocketService from '../lib/websocketService';

interface TaskFormProps {
  userId: string;
  onTaskCreated: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ userId, onTaskCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [tags, setTags] = useState<string[]>([]);
  const [dueDate, setDueDate] = useState<string>('');
  const [reminderTime, setReminderTime] = useState<string>('');
  const [recurrencePattern, setRecurrencePattern] = useState<string>('');
  const [recurrenceInterval, setRecurrenceInterval] = useState<number>(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const webSocketService = WebSocketService.getInstance();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

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
      const taskData: any = {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        tags: tags.join(','), // Convert array to comma-separated string
        due_date: dueDate || undefined,
        reminder_time: reminderTime || undefined,
        recurrence_pattern: recurrencePattern || undefined,
        recurrence_interval: recurrenceInterval || undefined,
      };

      const result = await taskApi.createTask(userId, taskData);

      if (result.error) {
        setError(result.error);
      } else {
        // Reset form
        setTitle('');
        setDescription('');
        setPriority('medium');
        setTags([]);
        setDueDate('');
        setReminderTime('');
        setRecurrencePattern('');
        setRecurrenceInterval(1);
        
        // Notify parent component
        onTaskCreated();
      }
    } catch (err) {
      setError('Failed to create task');
      console.error('Task creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTag = (tag: string) => {
    if (tag.trim() && !tags.includes(tag.trim())) {
      setTags([...tags, tag.trim()]);
    }
  };

  const handleRemoveTag = (index: number) => {
    const newTags = [...tags];
    newTags.splice(index, 1);
    setTags(newTags);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">Create New Task</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter task title (1-200 characters)"
            disabled={loading}
            maxLength={200}
          />
          <p className="mt-1 text-xs text-gray-500">
            {title.length}/200 characters
          </p>
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Enter task description (optional, max 1000 characters)"
            rows={3}
            disabled={loading}
            maxLength={1000}
          />
          <p className="mt-1 text-xs text-gray-500">
            {description.length}/1000 characters
          </p>
        </div>

        {/* Priority Selection */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <TaskPriority priority={priority} setPriority={setPriority} />
        </div>

        {/* Tags Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tags
          </label>
          <TaskTags tags={tags} onAddTag={handleAddTag} onRemoveTag={handleRemoveTag} />
        </div>

        {/* Due Date and Reminder */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Due Date and Reminder
          </label>
          <TaskDueDate 
            dueDate={dueDate} 
            reminderTime={reminderTime} 
            onDueDateChange={setDueDate} 
            onReminderChange={setReminderTime} 
          />
        </div>

        {/* Recurrence Pattern */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Recurrence
          </label>
          <TaskRecurrence
            recurrencePattern={recurrencePattern}
            recurrenceInterval={recurrenceInterval}
            onPatternChange={setRecurrencePattern}
            onIntervalChange={setRecurrenceInterval}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-md text-white ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
          } transition-colors duration-200`}
        >
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
};

export default TaskForm;