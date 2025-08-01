from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

app = FastAPI()
clients = {}
users = {}
app.mount("/static", StaticFiles(directory="static"), name="static")

class User(BaseModel):
    username: str
    password: str

@app.get("/")
async def get():
    return HTMLResponse(open("templates/index.html").read())

@app.post("/signup")
def signup(user: User):
    if user.username in users:
        return {"error": "Username already exists"}
    users[user.username] = user.password
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: User):
    for existing_user in users:
        print (f"Existing user: {existing_user}")
    if user.username in users and users[user.username] == user.password:
        print(f"User {user.username} logged in successfully")
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username ):
    await websocket.accept()
    for client in clients.values():
        await client.send_text(f"{username} has joined the chat")
    clients[username] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcasr to all connected clients
            for client in clients.values():
                await client.send_text(username+": "+data)
    except WebSocketDisconnect:
        del clients[username]
