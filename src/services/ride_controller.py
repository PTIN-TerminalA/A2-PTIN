from models.controller_model import DemanaCotxeRequest
from models.car_model import buscar_vehicle_disponible
from services.ws_manager import enviar_ruta_al_vehicle
import httpx

async def obtenir_ruta(origen, desti):
    url = "http://192.168.10.12/path"
    payload = {
        "start": [origen.x, origen.y],
        "goal": [desti.x, desti.y]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

async def processar_peticio(request: DemanaCotxeRequest):
    vehicle = await buscar_vehicle_disponible(request.origen)

    if not vehicle:
        return {"error": "No hi ha cap vehicle disponible"}

    ruta = await obtenir_ruta(request.origen, request.desti)

    await enviar_ruta_al_vehicle(vehicle.id, ruta)

    return {
        "vehicle_id": vehicle.id,
        "ruta": ruta
    }
