import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, WebSocket, Request, Form
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


@app.get("/admin/recent")
async def recent(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"recent_stills": CONNECTION_MANAGER.image_source.recent_stills},
    )


@app.get("/admin/still/{still_id}")
async def get_still(still_id: str, request: Request):
    still = CONNECTION_MANAGER.image_source.stills_by_id[still_id]
    if CONNECTION_MANAGER.image_source.rehydrate_for_admin_page:
        still.hydrate()
    return templates.TemplateResponse(
        request=request, name="still.html", context={"still": still}
    )


@app.post("/admin/still/{still_id}")
async def manage_still(still_id: str, action: Annotated[str, Form()], request: Request):
    still = CONNECTION_MANAGER.image_source.stills_by_id[still_id]
    if CONNECTION_MANAGER.image_source.rehydrate_for_admin_page:
        still.hydrate()
    if action == "deny":
        still.is_denylisted = True
    elif action == "allow":
        still.is_denylisted = False
    return templates.TemplateResponse(
        request=request, name="still.html", context={"still": still}
    )
