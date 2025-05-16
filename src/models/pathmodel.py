# controller_routes.py
from fastapi import APIRouter
from models.controller_model import DemanaCotxeRequest
from services.ride_controller import processar_peticio

router = APIRouter(prefix="/controller", tags=["Controller"])

@router.post("/demana-cotxe")
async def demanar_cotxe(request: DemanaCotxeRequest):
    resultat = await processar_peticio(request)
    return {"status": "ok", "assignat": resultat}