import uuid

from starlette.websockets import WebSocket

from app.schemas.chat_message import ChatMessage


class ConnectionManager:
    def __init__(self):
        self.id = 0
        self.clients = {}
        self.chat_history: list[ChatMessage] = []

    async def broadcast(self, websocket, message):

        chat_message = ChatMessage(id=uuid.uuid4().int, text=message, author_id=self.clients[websocket])
        self.chat_history.append(chat_message)
        for client_ws, _ in self.clients.items():
            try:
                await client_ws.send_text(chat_message.model_dump_json())
            except Exception as e:
                print(e)

    async def connect(self, websocket: WebSocket) -> int:
        await websocket.accept()

        self.clients[websocket] = self.id
        await websocket.send_json({"type": "init", "author_id": self.id})
        self.id += 1

        for chat_message in self.chat_history:
            await websocket.send_text(chat_message.model_dump_json())

        return self.id - 1

    def disconnect(self, websocket: WebSocket):
        del self.clients[websocket]
