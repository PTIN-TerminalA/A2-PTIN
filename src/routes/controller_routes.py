from fastapi import APIRouter
from models.controller_model import DemanaCotxeRequest
from services.ride_controller import processar_peticio
import logging

router = APIRouter(prefix="/controller", tags=["Controller"])

logger = logging.getLogger("ride_controller")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


@router.post("/demana-cotxe")
async def demanar_cotxe(request: DemanaCotxeRequest):
    logger.info(f"[{request.client.host}] Nova petició de cotxe per usuari_id={request.usuari_id} a lat={request.origen.lat}, lon={request.origen.lon}")
    resultat = await processar_peticio(request)
    
    if resultat:
        logger.info(f"Cotxe assignat a usuari {request.usuari_id}: vehicle_id={resultat.vehicle_id}, posició inicial={resultat.posicio}")
    else:
        logger.warning(f"No s'ha pogut assignar cap cotxe a l'usuari {request.usuari_id}")

    return {"status": "ok", "assignat": resultat}