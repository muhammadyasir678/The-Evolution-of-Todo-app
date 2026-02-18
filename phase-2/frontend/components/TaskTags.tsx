// TaskTags.tsx
import React, { useState } from 'react';

interface TaskTagsProps {
  tags: string;
  onChange: (tags: string) => void;
}

const TaskTags: React.FC<TaskTagsProps> = ({ tags, onChange }) => {
  const [inputValue, setInputValue] = useState('');

  // Convert comma-separated string to array for display
  const tagsArray = tags ? tags.split(',').map(tag => tag.trim()).filter(tag => tag) : [];

  const addTag = () => {
    if (inputValue.trim() && !tagsArray.includes(inputValue.trim())) {
      const newTagsArray = [...tagsArray, inputValue.trim()];
      onChange(newTagsArray.join(','));
      setInputValue('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    const newTagsArray = tagsArray.filter(tag => tag !== tagToRemove);
    onChange(newTagsArray.join(','));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag();
    }
  };

  return (
    <div className="flex flex-col">
      <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
      <div className="flex flex-wrap gap-2 mb-2">
        {tagsArray.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
          >
            {tag}
            <button
              type="button"
              className="flex-shrink-0 ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center text-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:outline-none focus:bg-indigo-500 focus:text-white"
              onClick={() => removeTag(tag)}
            >
              <span className="sr-only">Remove</span>
              <svg className="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                <path strokeLinecap="round" strokeWidth="1.5" d="M1 1l6 6m0-6L1 7" />
              </svg>
            </button>
          </span>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Add a tag..."
          className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full sm:text-sm border-gray-300 rounded-md"
        />
        <button
          type="button"
          onClick={addTag}
          className="ml-2 inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Add
        </button>
      </div>
    </div>
  );
};

export default TaskTags;