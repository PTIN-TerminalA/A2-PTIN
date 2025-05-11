import asyncio
import json
import logging as log
import ssl
import sys

from ssl import SSLContext
from uuid import UUID

import certifi
import websockets

from .peripherals.esp32 import Esp32
from .peripherals.location import PhysicalLocation, VirtualLocation
from .peripherals.powertrain import PhysicalPowertrain, VirtualPowertrain


class Car(Esp32):
    id: UUID
    ssl_context: SSLContext

    def __init__(
        self, id: UUID, serial_port: str, ignore: list[str], motor_interface: str, car_type: str, use_ssl: bool
    ):
        log.info(f"Creating new Car instance with ID {id}.")
        self.id = id
        self.car_type = car_type
        # print(f"Sóc {self.car_type}")

        self.use_ssl = use_ssl
        self.shutdown = 0

        if use_ssl:
            self.ssl_context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
            self.ssl_context.load_verify_locations(certifi.where())

        if self.car_type == "physical":
            self.location = PhysicalLocation()
            self.connect_serial(serial_port, ignore)

            self.powertrain = PhysicalPowertrain()
            self.powertrain.connect_powertrain(motor_interface)
        else:
            self.location = VirtualLocation()
            self.powertrain = VirtualPowertrain()

        log.info(f"Positioning and Powertrain configured correctly.")
        log.info(f"Car {id} ready.")

    async def connect_websocket(self, controller: str):
        log.info(f"Connecting websocket to {controller}...")
        # print(f"use_ssl és {self.use_ssl}")
        send_task = None
        receive_task = None
        try:
            async with websockets.connect(controller) as websocket:
                # Si es vol fer servir SSL, afegir el següent just entre "controller" i ")" -> , ssl=self.ssl_context if self.use_ssl else None
                # També s'ha d'afegir una segona 's' al "wss" que apareix a main.py
                log.info("Connected.")
                send_task = asyncio.create_task(self.send_location(websocket))
                receive_task = asyncio.create_task(
                    self.recieve_commands(websocket))

                while True:
                    await asyncio.sleep(1)
                    if self.shutdown:
                        break

        except KeyboardInterrupt:
            log.warn("Shutting down because KeyboardInterrupt was detected...")
            self.shutdown = 1

        except websockets.exceptions.ConnectionClosedError:
            log.error(
                "Websocket connection closed unexpectedly. Shutting down...")

        except Exception as e:
            log.error(f"Unexpected error in websocket connection: {e}")

        finally:
            if send_task:
                send_task.cancel()
            if receive_task:
                receive_task.cancel()
            log.warn("Disconnected from websocket.")
            sys.exit(1)

    async def send_location(self, websocket):
        while True:
            try:
                if self.car_type == "physical":
                    location = await self.get_ap_rssis()

                    log.debug("Sending location to websocket...")
                    await websocket.send(json.dumps({"location": location}))
                    log.debug("Location sent.")
                else:
                    # self.car_type == "virtual"
                    x_actual, y_actual = self.location.get()
                    orientacio_actual = self.powertrain.get_orientation()
                    data = {
                        "coordinates": {
                            "x": x_actual,
                            "y": y_actual,
                            "orientation": orientacio_actual
                        }
                    }
                    log.debug("Sending location to websocket...")
                    await websocket.send(json.dumps(data))
                    log.debug("Location sent.")

                await asyncio.sleep(0.5)  # Yield the websocket to other tasks

            except websockets.exceptions.ConnectionClosedError:
                log.error(
                    "Websocket disconnected while sending location. Stopping send_location task")
                self.shutdown = 1
                break  # Finalitzem la tasca sortint del bucle while

            except Exception as e:
                log.error(f"Failed to send location to websocket: {e}")
                self.shutdown = 1
                break

    async def recieve_commands(self, websocket):
        while True:
            try:
                log.debug("Waiting for a new message from the websocket...")
                recieved = await websocket.recv()
                log.debug(f"Recieved new message from websocket: {recieved}")

                recieved = json.loads(recieved)
                log.debug("Parsed message to json succesfully.")

                # No match statement in python 3.9!!
                if recieved["command"] == "move":
                    if self.car_type == "physical":
                        direction = self.powertrain.Direction.from_str(
                            recieved["direction"])
                    else:
                        # self.car_type == "virtual"
                        direction = self.powertrain.Direction.from_str_virtual(
                            recieved["direction"], self.powertrain.orientation)
                    self.powertrain.move(direction)
                else:
                    log.warn(f"Unknown movement command received.")

            except KeyboardInterrupt:
                log.warn("Shutting down because KeyboardInterrupt was detected...")
                self.shutdown = 1
            except websockets.exceptions.ConnectionClosedError:
                log.error(
                    "Websocket disconnected while receiving commands. Stopping receive_commands task")
                self.shutdown = 1
                break  # Finalitzem la tarea sortint del bucle while
            except Exception as e:
                log.error(f"Failed to recieve from websocket: {e}")
                self.shutdown = 1
                break
