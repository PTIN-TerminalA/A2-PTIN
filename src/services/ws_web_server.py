import asyncio
import websockets
import json

connected_web_clients = set()

async def web_socket_server():
    async def handler(websocket):
        print("Client Web connectat")
        connected_web_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            connected_web_clients.remove(websocket)

    print("Servidor WebSocket per a la Web en marxa al port 8766")
    async with websockets.serve(handler, "0.0.0.0", 8766):
        await asyncio.Future()  # no acaba mai

async def broadcast_position_to_web(position):
    for client in connected_web_clients:
        await client.send(json.dumps(position))
