/**
 * Chat API Client - Task T063
 * Implements sendMessage function that accepts conversation_id, message, user_id
 * Extracts JWT from Better Auth and makes POST request to /api/{user_id}/chat
 */

interface SendMessageParams {
  conversation_id: number | null;
  message: string;
  user_id: string;
}

interface SendMessageResponse {
  conversation_id: number;
  response: string;
  tool_calls: string[];
}

// Task T075: Add error handling for API client
export const sendMessage = async (params: SendMessageParams): Promise<SendMessageResponse> => {
  const { conversation_id, message, user_id } = params;

  try {
    // Extract JWT from Better Auth
    const token = await getCurrentUserToken(); // This would be replaced with actual Better Auth call

    // Validate inputs
    if (!user_id || !message.trim()) {
      throw new Error('Invalid input: user_id and non-empty message are required');
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user_id}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        conversation_id,
        message,
      }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized: Please log in again');
      } else if (response.status === 403) {
        throw new Error('Forbidden: You do not have permission to access this resource');
      } else if (response.status === 404) {
        throw new Error('Not found: The requested resource does not exist');
      } else if (response.status === 429) {
        throw new Error('Too many requests: Please try again later');
      } else if (response.status === 500) {
        throw new Error('Server error: Unable to process your request');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();

    // Validate response data
    if (!data.conversation_id || typeof data.response !== 'string') {
      throw new Error('Invalid response format from server');
    }

    return data;
  } catch (error: any) {
    console.error('Error sending message:', error);

    // Re-throw specific error messages
    if (error.message.includes('Network Error')) {
      throw new Error('Network error: Please check your internet connection');
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Connection error: Unable to reach the server');
    }

    // Re-throw the error to be handled by the calling component
    throw error;
  }
};

// Task T078: Add user authentication integration to chat interface
// Implementation for Better Auth integration
const getCurrentUserToken = async (): Promise<string> => {
  // In a real implementation, this would use Better Auth's client
  // For now, we'll simulate getting the token from auth state
  // In practice, this would use something like better-auth's getSession or token management

  // This is a simplified approach - in a real app, you would:
  // import { getClient } from 'better-auth/client'
  // const client = getClient()
  // const session = await client.getSession()
  // return session?.token || ''

  // For this implementation, we'll assume the token is available in localStorage
  // which would be set by the Better Auth provider
  const authData = localStorage.getItem('better-auth-session');
  if (authData) {
    try {
      const session = JSON.parse(authData);
      return session.token || session.accessToken || '';
    } catch (e) {
      console.warn('Could not parse auth session from localStorage');
      return '';
    }
  }
  return '';
};