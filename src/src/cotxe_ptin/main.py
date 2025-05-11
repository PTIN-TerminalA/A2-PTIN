__version__ = "0.1.2"

import asyncio
import logging
import os
import time

from .car import Car

logging.getLogger().setLevel(level=os.getenv("CAR_LOG_LEVEL", "INFO").upper())


async def main():
    id = os.getenv("CAR_ID", "00000000-0000-0000-0000-000000000000")
    serial_port = os.getenv("CAR_SERIAL_PORT", "/dev/ttyUSB0")
    ignore = [
        ap.strip() for ap in os.getenv("CAR_AP_IGNORE", "").split(",") if ap.strip()
    ]
    # canviar wss per ws quan no es vulgui fer servir SSL
    connexio = "ws://0.0.0.0:8765"
    controller = os.getenv("CAR_CONTROLLER", connexio)

    car_type = os.getenv("CAR_TYPE", "virtual")

    # print(f"Sóc {car_type}")

    use_ssl = False

    car = Car(id, serial_port, ignore, "/dev/i2c-7", car_type, use_ssl)
    await car.connect_websocket(controller)

    while True:
        time.sleep(1)

"""
def run_main():
    asyncio.run(main())
    # S'ha d'executar la corutina main amb un bucle d'events, no es pot cridar directament al main
    # Aquesta funció serà el punt d'entrada de la imatge de Docker (definit a setup.py)
    # Sense aquesta funció, quan s'executés el docker que conté aquest programa es cridaria directament a main sense asyncio
"""

if __name__ == "__main__":
    asyncio.run(main())
