import json
import logging as log
from serial import Serial
import time


class Esp32:
    BAUD_RATE = 115200
    MEASUREMENT_START = ">>>MEASUREMENT>>>"
    MEASUREMENT_END = "<<<MEASUREMENT<<<"

    serial_port: Serial
    ignore: list[str]

    def connect_serial(self, serial_port: str, ignore: list[str]):
        log.info(f"Connecting to serial port {serial_port}...")
        self.serial_port = Serial(serial_port, self.BAUD_RATE, timeout=1)
        log.info(f"Connected to {serial_port} with {self.BAUD_RATE} baud.")

        log.info(f"Ignoring the following BSSIDs for the AP scan: {ignore}")
        self.ignore = ignore

    async def get_ap_rssis(self) -> dict:
        access_points = []

        recieving = False

        while True:
            # If there's nothing in the serial port, wait for a bit and check again
            if self.serial_port.in_waiting <= 0:
                time.sleep(0.2)
                continue

            line = self.serial_port.readline().decode("utf-8").rstrip()

            if not recieving:
                if line.startswith(self.MEASUREMENT_START):
                    log.debug(
                        "Recieving a new AP measurement from the serial port.")
                    recieving = True

                continue

            # If we're not recieving, check if we should and jump to the next iteration
            else:
                if line.startswith(self.MEASUREMENT_END):
                    log.debug(
                        "Finished recieving a new AP measurement from the serial port."
                    )
                    return access_points

            # If we reached this point it means we're recieving a measurement
            log.debug(f"AP Measurement line recieved: {line}")
            measurement = json.loads(line)
            bssid = measurement.get("bssid")
            rssi = measurement.get("rssi")

            if bssid and rssi is not None and bssid not in self.ignore:
                access_points.append(
                    {
                        "bssid": bssid,
                        "rssi": rssi,
                    }
                )
