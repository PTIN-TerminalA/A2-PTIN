from fastapi import HTTPException
from fastapi.responses import JSONResponse
from models.path_model import Point, Path
from models.car_model import Car, load_all_cars, update_car
import redis
import uuid
import math

def calcular_distancia(origen: Point, desti: Point) -> float:
    return ((origen.x - desti.x) ** 2 + (origen.y - desti.y) ** 2) ** 0.5

def iniciar_trasllat(posicio_client: Point):
    try:
        db = redis.Redis(host="localhost", port=6379, db=0)
        cotxes = load_all_cars(db)

        disponibles = [c for c in cotxes if not c.working]
        if not disponibles:
            raise HTTPException(status_code=404, detail="No hi ha cap vehicle lliure")

        seleccionat = min(disponibles, key=lambda c: calcular_distancia(c.position, posicio_client))

        ruta = Path(
            id=str(uuid.uuid4()),
            path=[seleccionat.position, posicio_client]
        )

        seleccionat.working = True
        seleccionat.currentPath = ruta
        update_car(db, seleccionat)

        return JSONResponse(content={
            "vehicle": seleccionat.id,
            "inici": seleccionat.position.dict(),
            "destinacio": posicio_client.dict(),
            "ruta_id": ruta.id
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))