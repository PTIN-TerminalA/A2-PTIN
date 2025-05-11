import asyncio
import websockets
import json

clients = set()

async def ws_handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Posició rebuda del cotxe: {data}")
    finally:
        clients.remove(websocket)

async def send_command_to_all(command: dict):
    if clients:
        for ws in clients:
            await ws.send(json.dumps(command))
        print(f"Comanda enviada a {len(clients)} client(s): {command}")
    else:
        print("⚠️ Cap client connectat")

async def start_ws_server():
    print("WebSocket server escoltant al port 8765 (integrat amb FastAPI)")
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # no s'atura

        # import asyncio
# import websockets
# import json

# clients = set()

# async def handler(websocket):
#     clients.add(websocket)
#     try:
#         async for message in websocket:
#             data = json.loads(message)
#             print(f"Posició rebuda del cotxe: {data}")
#             # Aquí podrías guardar en Redis si quisieras
#     except websockets.exceptions.ConnectionClosed:
#         print("Cotxe desconnectat")
#     finally:
#         clients.remove(websocket)

# async def send_command_to_all(command):
#     if clients:
#         for ws in clients:
#             await ws.send(json.dumps(command))
#         print(f"Comanda enviada a {len(clients)} client(s)")
#     else:
#         print("Cap client connectat")

# async def main():
#     async with websockets.serve(handler, "0.0.0.0", 8765):
#         print("Server WebSocket esperant connexions al port 8765")
#         await asyncio.Future()  # Manté actiu

# # Lanza el servidor WebSocket
# if __name__ == "__main__":
#     asyncio.run(main())
