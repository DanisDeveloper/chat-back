import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from connection_manager import ConnectionManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.204.87","http://192.168.226.219", "http://localhost:5173"],  # Разрешенные домены
    allow_methods=["*"],
    allow_headers=["*"]
)

connection_manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, workers=1)
