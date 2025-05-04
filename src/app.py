from fastapi import FastAPI
from routes.ride_routes import router as ride_router
from routes.controller_routes import router as controller_router

app = FastAPI()

# Incloure aquí routers
app.include_router(ride_router)
app.include_router(controller_router)
