'use client';

import React, { useState, useEffect } from 'react';
import { signOut } from '../lib/auth';
import { FiLogOut } from 'react-icons/fi';

interface HeaderProps {
  userEmail?: string;
  userName?: string;
}

const Header: React.FC<HeaderProps> = ({ userEmail: initialUserEmail, userName: initialUserName }) => {
  const [userEmail, setUserEmail] = useState<string | undefined>(undefined);
  const [userName, setUserName] = useState<string | undefined>(undefined);
  const [hasMounted, setHasMounted] = useState(false);

  useEffect(() => {
    // Set the user data after mounting to ensure hydration consistency
    setUserEmail(initialUserEmail);
    setUserName(initialUserName);
    setHasMounted(true);
  }, [initialUserEmail, initialUserName]);

  const handleSignOut = async () => {
    try {
      await signOut();
      // Optionally redirect to sign-in page after sign-out
      window.location.href = '/signin';
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  // If not mounted yet, render a skeleton to prevent hydration mismatch
  if (!hasMounted) {
    return (
      <header className="bg-indigo-600 text-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold">Todo App</h1>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={handleSignOut}
              className="flex items-center space-x-1 bg-red-500 hover:bg-red-600 px-3 py-2 rounded-md transition-colors duration-200"
            >
              <FiLogOut />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </header>
    );
  }

  return (
    <header className="bg-indigo-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold">Todo App</h1>
          {userName && <p className="text-sm opacity-80">Welcome, {userName}</p>}
        </div>

        <div className="flex items-center space-x-4">
          {userEmail && (
            <span className="text-sm opacity-90">{userEmail}</span>
          )}
          <button
            onClick={handleSignOut}
            className="flex items-center space-x-1 bg-red-500 hover:bg-red-600 px-3 py-2 rounded-md transition-colors duration-200"
          >
            <FiLogOut />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;