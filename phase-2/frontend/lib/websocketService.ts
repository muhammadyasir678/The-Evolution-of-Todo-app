import { Task } from './types';

interface WebSocketEvent {
  event_id: string;
  user_id: string;
  task_id: string;
  action: string;
  task_data: Partial<Task>;
  timestamp: string;
  correlation_id: string;
  source_service: string;
}

class WebSocketService {
  private static instance: WebSocketService;
  private ws: WebSocket | null = null;
  private userId: string | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 5000; // 5 seconds
  private listeners: Array<(event: WebSocketEvent) => void> = [];

  public static getInstance(): WebSocketService {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  public connect(userId: string): void {
    // Check if WebSocket is supported in the current environment
    if (typeof WebSocket === 'undefined') {
      console.warn('WebSocket is not supported in this environment');
      return;
    }

    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      if (this.userId === userId) {
        // Already connected to the same user
        return;
      } else {
        // Disconnect from previous user
        this.disconnect();
      }
    }

    // Update the user ID
    this.userId = userId;

    // Check if WebSocket is supported in the current environment
    if (typeof WebSocket === 'undefined') {
      console.info('WebSocket is not supported in this environment, real-time updates will be disabled');
      return;
    }

    // For now, disable WebSocket functionality since the backend doesn't support it
    // In a production environment, you would check if the backend supports WebSocket
    console.info('WebSocket functionality is temporarily disabled, real-time updates will be disabled');
    return;
  }

  public disconnect(): void {
    // WebSocket is disabled, nothing to disconnect
    console.info('WebSocket is disabled, no disconnection needed');
    this.userId = null;
  }

  public subscribe(callback: (event: WebSocketEvent) => void): () => void {
    this.listeners.push(callback);
    
    // Return unsubscribe function
    return () => {
      const index = this.listeners.indexOf(callback);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  public isConnected(): boolean {
    // WebSocket is disabled
    return false;
  }

  public getConnectionStatus(): string {
    // WebSocket is disabled
    return 'disabled';
  }
}

export default WebSocketService;