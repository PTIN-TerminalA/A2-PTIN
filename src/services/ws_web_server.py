import asyncio
import websockets
import json

# Clients web connectats
connected_web_clients = set()

async def web_socket_server():
    async def handler(websocket):
        # Aquest codi només s'executa quan un client s'ha connectat
        print("Client Web connectat")
        connected_web_clients.add(websocket)
        try:
            await websocket.wait_closed()  # Espera fins que es tanqui la connexió
        finally:
            connected_web_clients.remove(websocket)
            print("Client Web desconnectat")

    print("Servidor WebSocket per a la Web en marxa al port 8766")
    async with websockets.serve(handler, "0.0.0.0", 8766):
        await asyncio.Future()  # Manté el servidor actiu per sempre

async def broadcast_position_to_web(position):
    disconnected = []
    for client in connected_web_clients:
        try:
            await client.send(json.dumps(position))
        except websockets.exceptions.ConnectionClosed:
            disconnected.append(client)

    # Elimina clients desconnectats
    for client in disconnected:
        connected_web_clients.discard(client)
