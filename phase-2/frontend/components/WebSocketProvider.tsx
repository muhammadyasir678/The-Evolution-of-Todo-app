'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import WebSocketService from '../lib/websocketService';

interface WebSocketContextType {
  isConnected: boolean;
  connectionStatus: string;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

interface WebSocketProviderProps {
  children: ReactNode;
  userId: string;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children, userId }) => {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [isConnected, setIsConnected] = useState(false);
  const webSocketService = WebSocketService.getInstance();

  useEffect(() => {
    // Connect to WebSocket when component mounts
    webSocketService.connect(userId);

    // Update connection status
    const updateStatus = () => {
      const status = webSocketService.getConnectionStatus();
      setConnectionStatus(status);
      setIsConnected(webSocketService.isConnected());
    };

    // Update status initially and whenever it changes
    updateStatus();
    const interval = setInterval(updateStatus, 1000); // Update every second

    // Cleanup on unmount
    return () => {
      clearInterval(interval);
      // Only disconnect if this is the last consumer
      // In a real implementation, you'd want more sophisticated connection management
    };
  }, [userId]);

  const value = {
    isConnected,
    connectionStatus,
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};