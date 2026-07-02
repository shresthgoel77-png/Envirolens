from fastapi import WebSocket
from typing import List
from core.logger import logger


class ConnectionManager:
    def __init__(self):
        # Keeps track of all actively connected UI clients
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts an incoming connection and registers it to the pool."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Frontend client connected via WebSocket. Active sessions: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Safely removes a client from the tracking pool."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Remaining active sessions: {len(self.active_connections)}")

    async def broadcast_json(self, data: dict):
        """Pushes data in real-time to all connected dashboards."""
        logger.debug(f"Broadcasting alert metadata to {len(self.active_connections)} clients.")
        
        # Iterate backwards over a shallow copy to safely remove disconnected sessions during loops
        for connection in list(self.active_connections):
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Failed to push message to a WebSocket client: {str(e)}")
                self.disconnect(connection)


# Shared global instance across the application
socket_manager = ConnectionManager()