import asyncio
import websockets
import json

async def cotxe_virtual():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Cotxe connectat al controller")
        while True:
            command = await websocket.recv()
            print(f"Comanda rebuda: {command}")
            await asyncio.sleep(2)
            pos = {
                "coordinates": {
                    "x": 5.0,
                    "y": 8.0,
                    "orientation": "north"
                }
            }
            await websocket.send(json.dumps(pos))

if __name__ == "__main__":
    asyncio.run(cotxe_virtual())
