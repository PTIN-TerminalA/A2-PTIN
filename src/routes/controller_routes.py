from fastapi import APIRouter
from models.controller_model import CommandRequest, PositionReport
from services.websocket_server import send_command_to_all

router = APIRouter(prefix="/controller", tags=["Controller"])

@router.post("/position")
def rebre_posicio(data: PositionReport):
    pos = data.coordinates
    print(f"Posició: x={pos.x}, y={pos.y}, orientació={pos.orientation}")
    return {
        "status": "posició rebuda",
        "detail": {
            "x": pos.x,
            "y": pos.y,
            "orientation": pos.orientation
        }
    }

@router.post("/command")
async def enviar_comanda(data: CommandRequest):
    await send_command_to_all(data.model_dump())
    return {"status": "ok", "detail": data.model_dump()}

