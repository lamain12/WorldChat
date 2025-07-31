from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

api = FastAPI()
clients = []

@app.get("/")
async def get():
    return HTMLResponse(open("templates/index.html").read())

