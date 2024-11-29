import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from stillframe.image_source import FileWalkerImageSource


class ConnectionManager:
    def __init__(self, image_source: FileWalkerImageSource):
        self.image_source = image_source
        self.active_connections: list[WebSocket] = []
        self.current_image: bytes = self.build_message()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_bytes(self.current_image)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: bytes):
        for connection in self.active_connections:
            try:
                await connection.send_bytes(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

    def build_message(self):
        return self.image_source.get_next_still()

    async def serve_forever(self):
        while True:
            self.current_image = self.build_message()
            await self.broadcast(self.current_image)
            await asyncio.sleep(1)
