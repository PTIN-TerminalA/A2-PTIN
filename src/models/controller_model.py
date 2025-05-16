from pydantic import BaseModel
from typing import Literal

class Punt(BaseModel):
    x: float
    y: float

class DemanaCotxeRequest(BaseModel):
    origen: Punt
    desti: Punt
    usuari: str
#quitar usuari