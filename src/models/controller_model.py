from pydantic import BaseModel
from typing import Literal

class Punt(BaseModel):
    x: float
    y: float

class DemanaCotxeRequest(BaseModel):
    desti: Punt
    usuari: str
#quitar usuari