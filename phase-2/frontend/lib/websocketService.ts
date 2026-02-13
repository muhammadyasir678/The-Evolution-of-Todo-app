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

    // Construct WebSocket URL - in production, this would come from environment variables
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/${userId}`;
    
    // For local development, we might need to connect to a specific WebSocket service
    // This URL assumes the WebSocket service is accessible at the same host
    const localWsUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL || `ws://localhost:8001/ws/${userId}`;
    const urlToUse = process.env.NODE_ENV === 'production' ? wsUrl : localWsUrl;

    console.log(`Connecting to WebSocket: ${urlToUse}`);
    
    this.ws = new WebSocket(urlToUse);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0; // Reset reconnect attempts on successful connection
    };

    this.ws.onmessage = (event) => {
      try {
        const eventData: WebSocketEvent = JSON.parse(event.data);
        console.log('Received WebSocket event:', eventData);
        
        // Notify all listeners
        this.listeners.forEach(listener => listener(eventData));
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      
      // Attempt to reconnect if we haven't exceeded max attempts
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          console.log(`Attempting to reconnect... (${++this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          this.connect(userId);
        }, this.reconnectInterval);
      } else {
        console.error('Max reconnection attempts reached');
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  public disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.userId = null;
    }
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
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  public getConnectionStatus(): string {
    if (!this.ws) return 'disconnected';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting';
      case WebSocket.OPEN:
        return 'connected';
      case WebSocket.CLOSING:
        return 'closing';
      case WebSocket.CLOSED:
        return 'closed';
      default:
        return 'unknown';
    }
  }
}

export default WebSocketService;