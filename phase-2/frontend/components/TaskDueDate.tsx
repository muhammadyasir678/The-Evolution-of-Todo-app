// TaskDueDate.tsx
import React, { useState } from 'react';

interface TaskDueDateProps {
  dueDate: string | null;
  reminderTime: string | null;
  onDueDateChange: (date: string | null) => void;
  onReminderChange: (time: string | null) => void;
}

const TaskDueDate: React.FC<TaskDueDateProps> = ({ 
  dueDate, 
  reminderTime, 
  onDueDateChange, 
  onReminderChange 
}) => {
  const [showReminder, setShowReminder] = useState(!!reminderTime);

  const handleReminderToggle = () => {
    if (showReminder) {
      // Turn off reminder
      setShowReminder(false);
      onReminderChange(null);
    } else {
      // Turn on reminder - default to 1 hour before due date
      setShowReminder(true);
      if (dueDate) {
        const dueDateTime = new Date(dueDate);
        dueDateTime.setHours(dueDateTime.getHours() - 1); // 1 hour before
        onReminderChange(dueDateTime.toISOString());
      }
    }
  };

  const handleDueDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = e.target.value ? e.target.value : null;
    onDueDateChange(newDate);
    
    // If reminder was set and due date changed, update reminder time too
    if (reminderTime && newDate) {
      const dueDateTime = new Date(newDate);
      dueDateTime.setHours(dueDateTime.getHours() - 1); // 1 hour before
      onReminderChange(dueDateTime.toISOString());
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
        <input
          type="datetime-local"
          value={dueDate || ''}
          onChange={handleDueDateChange}
          className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
        />
      </div>

      <div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="enable-reminder"
            checked={showReminder}
            onChange={handleReminderToggle}
            className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
          <label htmlFor="enable-reminder" className="ml-2 block text-sm text-gray-700">
            Enable Reminder
          </label>
        </div>

        {showReminder && (
          <div className="mt-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Reminder Time</label>
            <input
              type="datetime-local"
              value={reminderTime || ''}
              onChange={(e) => onReminderChange(e.target.value || null)}
              className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskDueDate;