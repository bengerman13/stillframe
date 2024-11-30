import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from stillframe.image_source import FileWalkerImageSource


class ConnectionManager:
    def __init__(self, image_source: FileWalkerImageSource):
        self.image_source = image_source
        self.active_connections: list[WebSocket] = []
        self.current_still = self.get_next_still()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_still(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_still(self, websocket: WebSocket):
        try:
            await websocket.send_text(self.current_still.to_json())
        except WebSocketDisconnect:
            self.disconnect(websocket)

    async def broadcast_still(self):
        for connection in self.active_connections:
            await self.send_still(connection)

    def get_next_still(self):
        self.current_still = self.image_source.get_next_still()

    async def serve_forever(self):
        while True:
            self.get_next_still()
            await self.broadcast_still()
            await asyncio.sleep(1)
