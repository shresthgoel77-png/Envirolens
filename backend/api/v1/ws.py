from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.manager import socket_manager
from core.logger import logger

router = APIRouter(tags=["WebSockets"])


@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time endpoint for pushing pollution anomaly updates directly to frontends."""
    await socket_manager.connect(websocket)
    try:
        # Keep connection open and await incoming heartbeats or messages from client
        while True:
            # Next.js can send text data or pings; we parse it here if needed
            _ = await websocket.receive_text()
            
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
        
    except Exception as e:
        logger.error(f"Unexpected WebSocket failure: {str(e)}", exc_info=True)
        socket_manager.disconnect(websocket)