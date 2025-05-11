from fastapi import APIRouter
from typing import List
from models.controller_model import CommandRequest
from services.ws_manager import send_command_to_all

router = APIRouter(prefix="/controller", tags=["Controller"])

@router.post("/commands")
async def enviar_comandes(data: List[CommandRequest]):
    for command in data:
        await send_command_to_all(command.model_dump())
    return {"status": "ok", "detail": [cmd.model_dump() for cmd in data]}
