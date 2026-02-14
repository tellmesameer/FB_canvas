from fastapi import FastAPI

from .routers import rooms, teams, match
from . import models, database
from .websocket import manager
from fastapi import WebSocket, WebSocketDisconnect
import json

# Create tables if not handled by Alembic (optional, but good for quick start if no migration run, though we did migration)
# models.Base.metadata.create_all(bind=database.engine) 

from fastapi.middleware.cors import CORSMiddleware

import logging
import sys

# Configure logging to write to file and console
# Create a custom logger
logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler("backend/server.log")
stream_handler = logging.StreamHandler(sys.stdout)

# Create formatters and add it to handlers
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Also force uvicorn logs to go to our file
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(file_handler)


app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000", # Common React port just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(teams.router)
app.include_router(match.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Backend server starting up...")

@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Parse data, validate, update state, broadcast
            # For now, echo/broadcast raw data for MVP logic or basic testing
            # Real implementation needs to handle specific message types ("move", "cursor", etc.)
            message = json.loads(data)
            await manager.broadcast(message, room_id, exclude=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        # Broadcast disconnect event
        await manager.broadcast({"type": "user_left", "client_id": client_id}, room_id)
    except Exception as e:
        logger.error(f"Error in websocket for client {client_id}: {e}")
        manager.disconnect(websocket, room_id)

@app.get("/")
def read_root():
    return {"Hello": "World"}
