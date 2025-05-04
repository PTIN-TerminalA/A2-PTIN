from fastapi import APIRouter
from models.path_model import Point
from controllers import ride_controller

router = APIRouter(prefix="/trasllats", tags=["Trasllats"])

@router.post("/iniciar")
def sol_trasllat(posicio: Point):
    return ride_controller.iniciar_trasllat(posicio)