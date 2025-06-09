from fastapi import WebSocket


class WSConnManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
       await websocket.accept()
       self.active_connections.append(websocket)

    async def send_json_data(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)
    
    async def send_text_data(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)
    
    def disconnect(self, websockets:WebSocket):
        self.active_connections.remove(websockets)
