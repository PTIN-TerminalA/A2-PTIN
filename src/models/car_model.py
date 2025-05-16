from typing import Optional

class Vehicle:
    def __init__(self, id, position, working):
        self.id = id
        self.position = position
        self.working = working

def buscar_vehicle_disponible(origen):
    # Retorna un vehicle fictici disponible
    return Vehicle("cotxe1", position=origen, working=False)