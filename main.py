from fastapi import FastAPI, WebSocket, Request, Response, WebSocketDisconnect, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

# instance for fastapi
app = FastAPI()

# basemodel class for register user


class RegisterValidator(BaseModel):
    username: str

    class Config:
        orm_mode = True

# class for the websocket connection


class ConnectionManager:
    # constructor for initializing the vairable
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    # method for WEBSOCKET connection
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # method for WEBSOCKET disconnection
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # method for broadcasting the message
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


# object for class ConnectionManager
manager = ConnectionManager()

# Jinja2 Templates to return frontend
templates = Jinja2Templates(directory="templates")

# User registration form is returning here HTML Response


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# HTML Response for the question page


@app.get("/questions", response_class=HTMLResponse)
async def handleform(request: Request):
    return templates.TemplateResponse("question.html", {"request": request})

# api for setting the cookie session


@app.post("/submit")
def read_user(user: RegisterValidator, response: Response):
    response.set_cookie(key="X-Authorization",
                        value=user.username, httponly=True)
    return {"error": 0, "message": "Registered Successfully"}

# created  api to get the username


@app.get("/user")
def getuserdetails(request: Request):
    user = request.cookies.get("X-Authorization")
    return {'details': user}


@app.websocket("/ws/question")
async def websocket_endpoint(websocket: WebSocket):

    # connect method of class ConnectionManager
    await manager.connect(websocket)

    # calling getuserdetails function for user details
    user = getuserdetails(websocket)
    socket_response = {'user': user['details'], 'message': 'got connected'}

    # calling the broadcast method for broadcasting the message
    await manager.broadcast(socket_response)
    try:
        while True:
            # reciving the data in json format
            data = await websocket.receive_json()

            # calling the broadcast method for broadcasting the message
            await manager.broadcast(data)
    except WebSocketDisconnect:

        # calling the disconnect method for disconnecting the socket of ConnectionManager class
        manager.disconnect(websocket)
        socket_response['message'] = 'got disconnected'

        # calling the broadcast method for broadcasting the message
        await manager.broadcast(socket_response)
