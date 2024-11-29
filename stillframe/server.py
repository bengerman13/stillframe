from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse

from stillframe.extensions import CONFIG, IMAGE_SOURCE

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>viewer</title>
    </head>
    <body style="margin: 0px;">
        <img id="liveImg" style="min-width: 100%; min-height: 100%; width: 100%; height: auto; position: fixed; top: 0; left: 0;" />
        <script>
            var img = document.getElementById("liveImg");
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.binaryType = 'arraybuffer';
            ws.onmessage = function(event) {
                var arrayBuffer = event.data;
                var blob  = new Blob([new Uint8Array(arrayBuffer)], {type: "image/bmp"});
                img.src = window.URL.createObjectURL(blob);
            };
        </script>
    </body>
</html>
"""

import asyncio


async def build_message(last: int):
    return IMAGE_SOURCE.get_next_still()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    last = 1
    while True:
        data = await build_message(last)
        await websocket.send_bytes(data)
        await asyncio.sleep(10)
