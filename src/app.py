import asyncio
from fastapi import FastAPI
from routes.controller_routes import router as controller_router
from services.ws_manager import start_ws_server
from services.ws_web_server import web_socket_server

app = FastAPI()
app.include_router(controller_router)

# Guardar referències a les tasques
background_tasks = []

@app.on_event("startup")
async def startup_event():
    task1 = asyncio.create_task(start_ws_server())
    task2 = asyncio.create_task(web_socket_server())
    background_tasks.extend([task1, task2])

@app.on_event("shutdown")
async def shutdown_event():
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)
