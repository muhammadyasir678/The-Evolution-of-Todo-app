// TaskRecurrence.tsx
import React from 'react';

interface TaskRecurrenceProps {
  recurrencePattern: string;
  recurrenceInterval: number;
  onPatternChange: (pattern: string) => void;
  onIntervalChange: (interval: number) => void;
}

const TaskRecurrence: React.FC<TaskRecurrenceProps> = ({
  recurrencePattern,
  recurrenceInterval,
  onPatternChange,
  onIntervalChange
}) => {
  const patterns = [
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'monthly', label: 'Monthly' },
  ];

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Recurrence Pattern</label>
        <select
          value={recurrencePattern}
          onChange={(e) => onPatternChange(e.target.value)}
          className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
        >
          <option value="">None</option>
          {patterns.map(pattern => (
            <option key={pattern.value} value={pattern.value}>
              {pattern.label}
            </option>
          ))}
        </select>
      </div>

      {recurrencePattern && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Repeat Every
          </label>
          <div className="flex items-center">
            <input
              type="number"
              min="1"
              value={recurrenceInterval}
              onChange={(e) => onIntervalChange(parseInt(e.target.value))}
              className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-20 sm:text-sm border-gray-300 rounded-md mr-2"
            />
            <span className="text-sm text-gray-500">
              {recurrencePattern === 'daily' && 'Day(s)'}
              {recurrencePattern === 'weekly' && 'Week(s)'}
              {recurrencePattern === 'monthly' && 'Month(s)'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskRecurrence;