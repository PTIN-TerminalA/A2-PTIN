from pydantic import BaseModel
from models.path_model import Point, Path
from typing import Optional
import redis
import json

class Car(BaseModel):
    id: str
    position: Point
    working: bool = False
    currentPath: Optional[Path] = None

    def to_json(self):
        return self.model_dump_json()

    @staticmethod
    def from_json(data: str):
        return Car.model_validate_json(data)

def load_all_cars(r: redis.Redis):
    cars = []
    for key in r.scan_iter("car:*"):
        data = r.get(key)
        if data:
            cars.append(Car.from_json(data))
    return cars

def update_car(r: redis.Redis, car: Car):
    r.set(f"car:{car.id}", car.to_json())