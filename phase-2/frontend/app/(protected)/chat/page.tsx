'use client';

/**
 * Chat Page - AI-Powered Todo Assistant
 * Protected route that imports ChatInterface component with proper layout
 * Task T078: Add user authentication integration to chat interface
 */

import React from 'react';
import ChatInterface from '../../../components/ChatInterface';
import Header from '../../../components/Header'; // Using the existing Header from phase-2
import { WebSocketProvider } from '../../../components/WebSocketProvider';

const ChatPage: React.FC = () => {
  // Using the same auth pattern as phase-2
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
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!session || !session.user) {
    // Redirect to sign in if not authenticated
    window.location.href = '/signin';
    return null;
  }

  // Use the actual user ID from the session data
  const actualUserId = session.user.id;

  return (
    <WebSocketProvider userId={actualUserId}>
      <div className="min-h-screen bg-gray-50">
        <Header userEmail={session.user.email} userName={session.user.name} />

        <main className="container mx-auto px-4 py-8">
          <div className="max-w-3xl mx-auto">
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-800">AI Todo Assistant</h1>
              <p className="text-gray-600">Chat with your personal todo assistant</p>
              {/* Task T078: Show user information */}
              <p className="text-sm text-gray-500 mt-1">Logged in as: {session.user.email}</p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-4 h-[600px] flex flex-col">
              <ChatInterface />
            </div>
          </div>
        </main>
      </div>
    </WebSocketProvider>
  );
};

export default ChatPage;