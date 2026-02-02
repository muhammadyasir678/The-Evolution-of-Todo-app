'use client';

import { useEffect } from 'react';
import { useSession } from '../lib/auth';

const Home = () => {
  const { data: session, isLoading } = useSession();

  useEffect(() => {
    if (!isLoading) {
      if (session) {
        // If user is logged in, redirect to tasks page
        window.location.href = '/tasks';
      } else {
        // If user is not logged in, redirect to sign in page
        window.location.href = '/signin';
      }
    }
  }, [session, isLoading]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Redirecting...</p>
      </div>
    </div>
  );
};

export default Home;