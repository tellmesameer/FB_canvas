from fastapi import WebSocket
from typing import List, Dict
import json
import logging

logger = logging.getLogger("backend")

class ConnectionManager:
    def __init__(self):
        # Store active connections: room_id -> list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        logger.info(f"Client connected to room {room_id}. Total connections: {len(self.active_connections[room_id])}")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
                logger.info(f"Client disconnected from room {room_id}")
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                logger.info(f"Room {room_id} is now empty and removed from active connections.")

    async def broadcast(self, message: dict, room_id: str, exclude: WebSocket = None):
        if room_id in self.active_connections:
            # Log broadcast event (maybe limit message size if too verbose)
            msg_type = message.get("type", "unknown")
            logger.info(f"Broadcasting message type '{msg_type}' to room {room_id}")
            
            for connection in self.active_connections[room_id]:
                if connection != exclude:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error broadcasting to client in room {room_id}: {e}")
                        # Could handle disconnect here too logic-wise

manager = ConnectionManager()
