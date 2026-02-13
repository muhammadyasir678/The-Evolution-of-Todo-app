'use client';

/**
 * Dashboard page for the Todo application
 * Provides access to both traditional task management and AI chat interface
 */

import React from 'react';
import { useRouter } from 'next/navigation';

const DashboardPage = () => {
  const router = useRouter();

  const [session, setSession] = React.useState<{ user: { id: string; email: string; name?: string } } | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    // Check for auth token in localStorage (same as phase-2 pattern)
    const token = localStorage.getItem('auth-token');

    if (!token) {
      // No token, redirect to sign in
      window.location.href = '/signin';
      return;
    }

    // Get user info from localStorage (same as phase-2 pattern)
    const userInfo = localStorage.getItem('user-info');
    if (userInfo) {
      try {
        const user = JSON.parse(userInfo);
        setSession({ user });
      } catch (error) {
        console.error('Failed to parse user info from localStorage', error);
        window.location.href = '/signin';
        return;
      }
    } else {
      window.location.href = '/signin';
      return;
    }

    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session || !session.user) {
    // Redirect to sign in if not authenticated
    window.location.href = '/signin';
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome to Todo Assistant</h1>
          <p className="text-gray-600 mb-8">Choose how you want to manage your tasks</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Traditional Task Management Card */}
            <div
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow duration-200 border border-gray-200"
              onClick={() => router.push('/tasks')}
            >
              <div className="flex items-center mb-4">
                <div className="bg-indigo-100 p-3 rounded-lg mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-gray-800">Traditional Tasks</h2>
              </div>
              <p className="text-gray-600 mb-4">Manage your tasks with familiar checkboxes and forms</p>
              <button className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition-colors duration-200">
                Go to Tasks
              </button>
            </div>

            {/* AI Chat Assistant Card */}
            <div
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow duration-200 border border-green-200"
              onClick={() => router.push('/chat')}
            >
              <div className="flex items-center mb-4">
                <div className="bg-green-100 p-3 rounded-lg mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-gray-800">AI Assistant</h2>
              </div>
              <p className="text-gray-600 mb-4">Talk to your AI assistant to manage tasks with natural language</p>
              <button className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors duration-200">
                Open Chat
              </button>
            </div>
          </div>

          <div className="mt-12 bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">About This App</h3>
            <p className="text-gray-600 mb-2">This Todo app offers two ways to manage your tasks:</p>
            <ul className="list-disc pl-5 text-gray-600 space-y-1">
              <li><strong>Traditional Interface</strong>: Classic task management with forms and lists</li>
              <li><strong>AI Assistant</strong>: Natural language interaction with an AI-powered assistant</li>
            </ul>
            <p className="text-gray-600 mt-3">Both interfaces work with the same task data, so your tasks are synchronized regardless of which interface you use.</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;