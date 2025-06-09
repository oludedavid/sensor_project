
from datetime import datetime
from fastapi import APIRouter, WebSocket
from app.src.utils.websocket import WSConnManager
import asyncio
import random

#initialise the websocket connection manager
ws_conn_manager = WSConnManager()

#initialise the websocket router
websocket_router = APIRouter()


@websocket_router.websocket("/sensor")
async def send_sensor_data(websocket: WebSocket):
    await ws_conn_manager.connect(websocket)
    try:
        while True:
            sensor_data = {
                "temperature": round(random.uniform(20.0, 30.0), 2),
                "humidity": round(random.uniform(40.0, 60.0), 2),
                "timestamp": datetime.utcnow().isoformat()
            }
            await ws_conn_manager.send_json_data(sensor_data)
            await asyncio.sleep(2)  # Send new data every 2 seconds
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        ws_conn_manager.disconnect(websocket)