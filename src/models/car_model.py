from typing import Optional
from services.ws_manager import vehicle_data
from enum import Enum

class VehicleState(Enum):
    Stopped = "stopped"
    Moving = "moving"
class Vehicle:
    def __init__(self, id, positionX, positionY, state):
        self.id = id
        self.positionX = positionX
        self.positionY = positionY
        self.state = state

def buscar_vehicle_disponible():
    # Retorna un vehicle fictici disponible
    # S'haura de fer una crida a la BBDD per obtenir el vehicle que estigui disponible
    # i que estigui més a prop de l'origen
    
    return Vehicle("cotxe1", positionX=0.5, positionY=0.5, state=VehicleState.Stopped)