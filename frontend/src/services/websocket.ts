import { useCanonicalStore } from '../store/canonicalStore';
import { useUIStore } from '../store/uiStore';

type MessageHandler = (data: any) => void;

class WebSocketService {
    private ws: WebSocket | null = null;
    private messageHandlers: Set<MessageHandler> = new Set();
    private reconnectInterval = 1000;
    private maxReconnectInterval = 30000;
    private url: string;
    private throttleMap: Map<string, number> = new Map(); // Key -> timestamp
    private throttleLimit = 50; // ms (approx 20fps)

    constructor() {
        const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const wsBase = apiBase.replace(/^http/, 'ws');
        this.url = wsBase;
    }

    connect(roomId: string, clientId: string) {
        if (this.ws) {
            this.ws.close();
        }

        const fullUrl = `${this.url}/ws/${roomId}/${clientId}`;
        console.log(`Connecting to ${fullUrl}`);

        this.ws = new WebSocket(fullUrl);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectInterval = 1000;
            useUIStore.getState().setIsConnected(true);
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
                this.messageHandlers.forEach(handler => handler(data));
            } catch (e) {
                console.error('Failed to parse WS message', e);
            }
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            useUIStore.getState().setIsConnected(false);
            this.scheduleReconnect(roomId, clientId);
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error', error);
            this.ws?.close();
        };
    }

    private handleMessage(message: any) {
        const canonicalStore = useCanonicalStore.getState();

        switch (message.type) {
            case 'snapshot':
                // Assuming message.data contains the room
                if (message.room) {
                    canonicalStore.setSnapshot(message.room);
                }
                break;
            case 'player_moved':
                // Directly update store
                if (message.player) {
                    canonicalStore.updatePlayer(message.player);
                }
                break;
            case 'match_status':
                if (message.status) {
                    canonicalStore.setMatchStatus(message.status);
                }
                break;
            // Add more cases as needed
        }
    }

    private scheduleReconnect(roomId: string, clientId: string) {
        setTimeout(() => {
            console.log(`Reconnecting in ${this.reconnectInterval}ms...`);
            this.connect(roomId, clientId);
            this.reconnectInterval = Math.min(this.reconnectInterval * 2, this.maxReconnectInterval);
        }, this.reconnectInterval);
    }

    send(data: any) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    // Throttled send for frequent updates like movement
    sendThrottled(key: string, data: any) {
        const now = Date.now();
        const lastSent = this.throttleMap.get(key) || 0;

        if (now - lastSent > this.throttleLimit) {
            this.send(data);
            this.throttleMap.set(key, now);
        }
    }

    subscribe(handler: MessageHandler) {
        this.messageHandlers.add(handler);
        return () => {
            this.messageHandlers.delete(handler);
        };
    }
}

export const wsService = new WebSocketService();
