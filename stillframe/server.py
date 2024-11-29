import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from stillframe.extensions import CONNECTION_MANAGER


@asynccontextmanager
async def lifespan(app: FastAPI):
    t = asyncio.create_task(CONNECTION_MANAGER.serve_forever())
    yield
    t.cancel()


app = FastAPI(lifespan=lifespan)


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
            function startWebsocket() {
                var ws = new WebSocket("ws://localhost:8000/ws");
                ws.binaryType = 'arraybuffer';
                ws.onmessage = function(event) {
                    var arrayBuffer = event.data;
                    var blob  = new Blob([new Uint8Array(arrayBuffer)], {type: "image/bmp"});
                    img.src = window.URL.createObjectURL(blob);
                };
                ws.onclose = function() {
                    ws = null;
                    setTimeout(startWebsocket, 1000);
                }
            }
            startWebsocket();
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await CONNECTION_MANAGER.connect(websocket)
    while True:
        await asyncio.sleep(1)
