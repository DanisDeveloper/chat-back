import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.204.87","http://192.168.226.219", "http://localhost:5173"],  # Разрешенные домены
    allow_methods=["*"],
    allow_headers=["*"]
)
clients = {}
i = 0


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global i
    await websocket.accept()
    if websocket not in clients:
        clients[websocket] = f"{i}"
        i += 1

    try:
        while True:
            data = await websocket.receive_text()
            for client_ws, _ in clients.items():
                try:
                    await client_ws.send_text(f"{clients[websocket]}: {data}")
                except Exception as e:
                    print(e)

    except WebSocketDisconnect:
        del clients[websocket]


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, workers=1)
