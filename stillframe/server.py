import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from stillframe.extensions import CONNECTION_MANAGER


@asynccontextmanager
async def lifespan(app: FastAPI):
    t = asyncio.create_task(CONNECTION_MANAGER.serve_forever())
    yield
    t.cancel()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse(request=request, name="client.html", context={})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await CONNECTION_MANAGER.connect(websocket)
    while True:
        await asyncio.sleep(1)
