// TaskFilters.tsx
import React from 'react';

interface FilterOptions {
  priority?: string;
  tags?: string;
  status?: string;
  dueDateRange?: { start?: string; end?: string };
}

interface TaskFiltersProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({ filters, onFilterChange }) => {
  const priorities = ['high', 'medium', 'low'];
  const statuses = ['all', 'pending', 'completed'];

  const handlePriorityChange = (priority: string) => {
    onFilterChange({
      ...filters,
      priority: priority !== 'all' ? priority : undefined
    });
  };

  const handleStatusChange = (status: string) => {
    onFilterChange({
      ...filters,
      status: status !== 'all' ? status : undefined
    });
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>

      {/* Priority Filter */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Priority</h4>
        <select
          value={filters.priority || 'all'}
          onChange={(e) => handlePriorityChange(e.target.value)}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          <option value="all">All Priorities</option>
          {priorities.map(priority => (
            <option key={priority} value={priority}>
              {priority.charAt(0).toUpperCase() + priority.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Status Filter */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Status</h4>
        <select
          value={filters.status || 'all'}
          onChange={(e) => handleStatusChange(e.target.value)}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          {statuses.map(status => (
            <option key={status} value={status}>
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Due Date Range Filter */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Due Date Range</h4>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs text-gray-500 mb-1">Start Date</label>
            <input
              type="date"
              value={filters.dueDateRange?.start || ''}
              onChange={(e) => onFilterChange({
                ...filters,
                dueDateRange: {
                  ...filters.dueDateRange,
                  start: e.target.value
                }
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">End Date</label>
            <input
              type="date"
              value={filters.dueDateRange?.end || ''}
              onChange={(e) => onFilterChange({
                ...filters,
                dueDateRange: {
                  ...filters.dueDateRange,
                  end: e.target.value
                }
              })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskFilters;