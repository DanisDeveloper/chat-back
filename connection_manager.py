from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.id = 0
        self.clients = {}
        self.chat_history = []

    async def broadcast(self, websocket, message):
        temp = f"{self.clients[websocket]}: {message}"
        self.chat_history.append(temp)
        for client_ws, _ in self.clients.items():
            try:
                await client_ws.send_text(temp)
            except Exception as e:
                print(e)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        if websocket not in self.clients:
            self.clients[websocket] = f"{self.id}"
            self.id += 1

            for message in self.chat_history:
                await websocket.send_text(message)


    def disconnect(self, websocket: WebSocket):
        del self.clients[websocket]
