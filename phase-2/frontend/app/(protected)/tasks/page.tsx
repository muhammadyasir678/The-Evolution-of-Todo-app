'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../../../components/Header';
import TaskForm from '../../../components/TaskForm';
import TaskList from '../../../components/TaskList';
import { WebSocketProvider } from '../../../components/WebSocketProvider';

const TasksPage = () => {
  const router = useRouter();
  const [session, setSession] = useState<{ user: { id: string; email: string; name?: string } } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasHydrated, setHasHydrated] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    // This ensures the effect only runs on the client side
    if (typeof window === 'undefined') {
      return;
    }

    // Check for auth token in localStorage
    const token = localStorage.getItem('auth-token');

    if (!token) {
      // No token, user is not authenticated
      setSession(null);
      setIsLoading(false);
      setHasHydrated(true);
      return;
    }

    // Get user info from localStorage (stored after login/signup)
    const userInfo = localStorage.getItem('user-info');
    if (userInfo) {
      try {
        const user = JSON.parse(userInfo);
        setSession({ user });
      } catch (error) {
        console.error('Failed to parse user info from localStorage', error);
        // If parsing fails, we can't reliably identify the user
        setSession(null);
      }
    } else {
      // If no user info is stored, we can't reliably identify the user
      // Even though there's a token, we don't know who the user is
      setSession(null);
    }

    setIsLoading(false);
    setHasHydrated(true);
  }, []);

  useEffect(() => {
    if (hasHydrated && (!session || !session.user)) {
      // Redirect to sign-in if not authenticated
      router.push('/signin');
    }
  }, [session, hasHydrated, router]);

  // Prevent hydration mismatch by ensuring client-side only rendering after hydration
  if (!hasHydrated) {
    // Return the same structure as the loading state to prevent mismatch
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isLoading || !hasHydrated) {
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
    // This should not normally render due to redirect, but included for safety
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting...</p>
        </div>
      </div>
    );
  }

  // Use the actual user ID from the session data
  const actualUserId = session.user.id;

  const handleTaskCreated = () => {
    // Trigger a refresh of the task list
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <WebSocketProvider userId={actualUserId}>
      <div className="min-h-screen bg-gray-50">
        <Header userEmail={session.user.email} userName={session.user.name} />

        <main className="container mx-auto px-4 py-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">Your Tasks</h1>

            <TaskForm
              userId={actualUserId}
              onTaskCreated={handleTaskCreated}
            />

            <TaskList key={`task-list-${refreshTrigger}`} userId={actualUserId} />
          </div>
        </main>
      </div>
    </WebSocketProvider>
  );
};

export default TasksPage;