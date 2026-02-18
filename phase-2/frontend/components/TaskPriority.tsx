// TaskPriority.tsx
import React from 'react';

interface TaskPriorityProps {
  priority: 'high' | 'medium' | 'low';
  setPriority: (priority: 'high' | 'medium' | 'low') => void;
}

const TaskPriority: React.FC<TaskPriorityProps> = ({ priority, setPriority }) => {
  const priorities = [
    { value: 'low', label: 'Low', color: 'text-blue-600 bg-blue-100' },
    { value: 'medium', label: 'Medium', color: 'text-yellow-600 bg-yellow-100' },
    { value: 'high', label: 'High', color: 'text-red-600 bg-red-100' },
  ];

  return (
    <div className="flex flex-col">
      <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
      <div className="flex space-x-2">
        {priorities.map((p) => (
          <button
            key={p.value}
            type="button"
            className={`px-3 py-1 rounded-full text-xs font-medium ${
              priority === p.value
                ? `${p.color} ring-2 ring-offset-2 ring-${p.value === 'high' ? 'red' : p.value === 'medium' ? 'yellow' : 'blue'}-500`
                : `${p.color.replace('bg-', 'bg-opacity-50 bg-').replace('text-', 'text-opacity-70 text-')}`
            }`}
            onClick={() => setPriority(p.value as 'high' | 'medium' | 'low')}
          >
            {p.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TaskPriority;