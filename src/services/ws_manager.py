from services.ws_web_server import broadcast_position_to_web
from models.controller_model import Punt
import ssl
import asyncio
import websockets
import json

# vehicle_data = { vehicle_id: {"coordinates": Punt(x, y), "state": "stopped" or "moving"} }
vehicle_data = {}

connected_clients = set()  # Ya definido si tienes el server websocket

async def enviar_ruta_al_vehicle(vehicle_id: str, ruta: list):
    msg = {
        "command": "set_path",
        "path": ruta
    }

    for client in connected_clients:
        await client.send(json.dumps(msg))

async def ws_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:    
            data = json.loads(message)
            
            vehicle_id = data.get("id")
            position = data.get("coordinates")
            state = data.get("state")
            
            if vehicle_id and position:
                vehicle_data[vehicle_id] = {
                    "position": Punt(x=position["x"], y=position["y"]),
                    "state": state
                }
                
            print(f"Vehicles actualitzats: {vehicle_data}")
            
            await broadcast_position_to_web(data)
    finally:
        connected_clients.remove(websocket)

async def send_command_to_all(command: dict):
    if connected_clients:
        for ws in connected_clients:
            await ws.send(json.dumps(command))
        print(f"Comanda enviada a {len(connected_clients)} client(s): {command}")
    else:
        print("Cap client connectat")

async def start_ws_server():
    print("WebSocket (cotxe) escoltant al port 8765 (integrat amb FastAPI)")
    
    '''
    # Crear context SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")
    
    async with websockets.serve(ws_handler, "0.0.0.0", 8765, ssl=ssl_context):
        await asyncio.Future()  # no
    '''
    
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # no s'atura



# connected_clients = set()

# async def enviar_ruta_al_vehicle(vehicle_id: str, ruta: list):
#     msg = {
#         "command": "set_path",
#         "path": ruta
#     }

#     for client in connected_clients:
#         await client.send(json.dumps(msg))


        