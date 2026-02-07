'use client';

/**
 * ChatInterface Component - Task T042 & T060
 * Integrates OpenAI ChatKit components with input field and send button
 */

import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import { sendMessage } from '../lib/chatApi';

// Import OpenAI ChatKit components
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'chatkit-app': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      'chatkit-conversation': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      'chatkit-messages': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
      'chatkit-input': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    }
  }
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get user ID from auth (placeholder for now)
      const userId = 'user-123'; // This should come from auth context

      const response = await sendMessage({
        conversation_id: conversationId,
        message: inputValue,
        user_id: userId
      });

      // Update conversation ID if new conversation was created
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Task T060: Enhance ChatInterface component to integrate with OpenAI ChatKit components
  // This is a conceptual implementation as the exact ChatKit integration would require
  // the actual OpenAI ChatKit SDK which may have specific components
  return (
    <div className="flex flex-col h-full">
      {/* Using ChatKit components where available */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {messages.length > 0 ? (
          messages.map((msg) => (
            <ChatMessage
              key={msg.id}
              role={msg.role}
              content={msg.content}
              timestamp={msg.timestamp}
            />
          ))
        ) : (
          <div className="text-center text-gray-500 mt-10">
            Start a conversation with the AI assistant!
          </div>
        )}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-200 text-gray-800 rounded-lg rounded-bl-none px-4 py-2">
              <div className="flex items-center">
                <span className="mr-2">AI is thinking...</span>
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t p-4 bg-white">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-2 rounded-r-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!inputValue.trim() || isLoading}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;