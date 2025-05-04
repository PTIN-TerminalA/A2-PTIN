import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

# Eliminar tots els cotxes existents
for key in r.scan_iter("car:*"):
    r.delete(key)
print("Tots els vehicles anteriors han estat eliminats.")

# Demanar nombre de cotxes a crear
num = int(input("Quants vehicles vols crear? "))

for i in range(num):
    print(f"\nVehicle {i+1}:")
    car_id = input("  ID del vehicle: ")
    x = float(input("  Posició X: "))
    y = float(input("  Posició Y: "))

    car = {
        "id": car_id,
        "position": {"x": x, "y": y},
        "working": False,
        "currentPath": None
    }

    r.set(f"car:{car_id}", json.dumps(car))
    print(f"  → Vehicle {car_id} creat correctament.")

print("\nTots els vehicles han estat afegits a Redis.")