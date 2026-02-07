// Custom auth implementation for the Todo app
// Since Better Auth client API is causing issues, we'll implement a simple auth client

// Define the types for our auth functions
type SignInOptions = {
  email: string;
  password: string;
};

type SignOutOptions = {
  callbackUrl?: string;
};

type SessionData = {
  user: {
    id: string;
    email: string;
    name?: string;
  } | null;
  expires?: string;
};

// Mock signIn function
export const signIn = async (options: SignInOptions): Promise<{ user?: any; error?: string }> => {
  try {
    const response = await fetch('/api/auth/signin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(options),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Sign in failed');
    }

    // Store token in localStorage or cookies if needed
    if (data.token) {
      localStorage.setItem('auth-token', data.token);
    }

    return { user: data.user };
  } catch (error: any) {
    return { error: error.message };
  }
};

// Mock signOut function
export const signOut = async (options?: SignOutOptions): Promise<{ success: boolean; error?: string }> => {
  try {
    // Remove token from localStorage or cookies
    localStorage.removeItem('auth-token');

    // Call backend signout endpoint if needed
    await fetch('/api/auth/signout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Redirect if callbackUrl is provided
    if (options?.callbackUrl) {
      window.location.href = options.callbackUrl;
    }

    return { success: true };
  } catch (error: any) {
    return { success: false, error: error.message };
  }
};

// Mock useSession hook
export const useSession = (): { data: SessionData | null; isLoading: boolean } => {
  // In a real implementation, this would use React state and effects
  // For now, we'll return a simple mock

  if (typeof window === 'undefined') {
    // Server-side
    return { data: null, isLoading: false };
  }

  // Client-side
  const token = localStorage.getItem('auth-token');

  if (!token) {
    return { data: { user: null }, isLoading: false };
  }

  // In a real implementation, we'd verify the token and get user info
  // For now, we'll return a mock user if token exists
  return {
    data: {
      user: {
        id: 'mock-user-id',
        email: 'user@example.com',
        name: 'Mock User'
      }
    },
    isLoading: false
  };
};