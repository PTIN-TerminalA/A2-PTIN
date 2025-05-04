import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

# Obtener el coche y modificarlo
car_id = "car1"
data = r.get(f"car:{car_id}")

if data:
    car = json.loads(data)
    car["working"] = False
    car["currentPath"] = None
    r.set(f"car:{car_id}", json.dumps(car))
    print(f"Vehicle {car_id} alliberat.")
else:
    print(f"No s'ha trobat el vehicle {car_id}.")
