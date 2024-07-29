from fastapi import (APIRouter, Request, WebSocket,
                     WebSocketDisconnect, Depends,
                     HTTPException, status)
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

templates = Jinja2Templates(directory='templates')


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get('/chat/')
def get_chat_page(request: Request):
    return templates.TemplateResponse('chat.html', {'request': request})


@router.websocket('/ws/')
async def connect_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = websocket.receive_text()
            await manager.send_personal_message(f'Your message {data}', websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


