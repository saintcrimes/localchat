from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:

    def __init__(self):
        self.chats: List[WebSocket] = []
        
    @property
    def quantity_of_websockets(self) -> int:
        return len(self.chats) 

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.chats.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.chats.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        dead_connection = []
        for connection in self.chats:
            try:
                await connection.send_text(message)
            except RuntimeError:
                dead_connection.append(connection)

        for connection in dead_connection:
            if connection in self.chats:
                self.chats.remove(connection)

    async def send_to_user(self, user_id: int, message: str) -> bool:
        sockets = self.active_connections.get(user_id, [])

        if not sockets:
            return False
        for ws in sockets:
            await ws.send_text(message)
        return True

manager = ConnectionManager()