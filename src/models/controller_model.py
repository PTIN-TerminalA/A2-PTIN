from pydantic import BaseModel
from typing import Literal, Dict

class CommandRequest(BaseModel):
    command: Literal["move"]
    direction: Literal["forward", "back", "right", "left"]

class Coordinates(BaseModel):
    x: float
    y: float
    orientation: Literal["north", "south", "east", "west"]

class PositionReport(BaseModel):
    coordinates: Coordinates