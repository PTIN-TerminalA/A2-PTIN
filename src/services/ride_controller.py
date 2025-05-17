from models.controller_model import DemanaCotxeRequest
from models.car_model import buscar_vehicle_disponible
from services.ws_manager import enviar_ruta_al_vehicle
import httpx
import logging

logger = logging.getLogger("ride_controller")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

async def obtenir_ruta(origen, desti):
    url = "http://192.168.10.12/path"
    payload = {
        "start": [origen.x, origen.y],
        "goal": [desti.x, desti.y]
    }
    
    logger.info(f"Sol·licitant ruta de {payload['start']} a {payload['goal']} a {url}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Ruta obtinguda amb èxit")
        return response.json()

async def processar_peticio(request: DemanaCotxeRequest):
    logger.info(f"Processant petició de cotxe per usuari_id={request.usuari_id} des de {request.origen} fins a {request.desti}")
    
    vehicle = await buscar_vehicle_disponible(request.origen)

    if not vehicle:
        logger.warning("No s'ha trobat cap vehicle disponible per la zona sol·licitada")
        return {"error": "No hi ha cap vehicle disponible"}

    logger.info(f"Vehicle {vehicle.id} assignat provisionalment. Obtenint ruta...")
    
    ruta = await obtenir_ruta(request.origen, request.desti)
    
    logger.debug(f"[TRAJECTE] vehicle {vehicle.id} rebrà ruta amb {len(ruta.get('path', []))} punts")

    await enviar_ruta_al_vehicle(vehicle.id, ruta)
    
    logger.info(f"Ruta enviada correctament al vehicle {vehicle.id}")

    return {
        "vehicle_id": vehicle.id,
        "ruta": ruta
    }
