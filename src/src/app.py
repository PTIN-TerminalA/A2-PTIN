import asyncio
from fastapi import FastAPI
from routes.controller_routes import router as controller_router
from services.ws_manager import start_ws_server

app = FastAPI()

# Incloure aquí routers
app.include_router(controller_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_ws_server())