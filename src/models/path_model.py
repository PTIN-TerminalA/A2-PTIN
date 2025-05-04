from pydantic import BaseModel
from typing import List

class Point(BaseModel):
    x: float
    y: float

class Path(BaseModel):
    id: str
    path: List[Point]