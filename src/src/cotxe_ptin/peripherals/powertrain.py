from enum import Enum
import logging as log
from typing import Tuple

from PCA9685_smbus2 import PCA9685
from .location import VirtualLocation


class Powertrain:
    class Direction(Enum):
        Forward = (2000, 2000, 2000, 2000)
        Back = (-2000, -2000, -2000, -2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)

        @staticmethod
        def from_str(direction: str):
            direction = direction.lower()

            # No match statement in python 3.9!!
            if direction == "forward":
                return Powertrain.Direction.Forward
            elif direction == "back":
                return Powertrain.Direction.Back
            elif direction == "left":
                return Powertrain.Direction.Left
            elif direction == "right":
                return Powertrain.Direction.Right
            else:
                log.warn("Stopping car due to unknown direction")
                return Powertrain.Direction.Stop

        @staticmethod
        def from_str_virtual(direction: str, orientation: str):
            if direction == "forward":
                if orientation == "north":
                    return (0, 1)
                elif orientation == "south":
                    return (0, -1)
                elif orientation == "east":
                    return (1, 0)
                elif orientation == "west":
                    return (-1, 0)

            elif direction == "back":
                if orientation == "north":
                    return (0, -1)
                elif orientation == "south":
                    return (0, 1)
                elif orientation == "east":
                    return (-1, 0)
                elif orientation == "west":
                    return (1, 0)

            elif direction == "left":
                gir = ["north", "west", "south", "east"]
                return gir[(gir.index(orientation) + 1) % 4]

            elif direction == "right":
                gir = ["north", "east", "south", "west"]
                return gir[(gir.index(orientation) + 1) % 4]
            else:
                log.warn("Stopping car due to unknown direction")
                return (0, 0)


class PhysicalPowertrain(Powertrain):
    # pwm: PCA9685

    class Motor(Enum):
        TopLeft = (0, 0, 1)
        TopRight = (1, 6, 7)
        BottomLeft = (2, 3, 2)
        BottomRight = (3, 4, 5)

    def connect_powertain(self, interface: str):
        log.info(f"Connecting to powertrain on interface {interface}...")
        self.pwm = PCA9685.PCA9685(interface=interface)
        self.pwm.set_pwm_freq(50)
        log.info("Successfully connected to and configured the powertrain.")

    def set_motor(self, motor: Motor, direction: Powertrain.Direction):
        (index, channel_a, channel_b) = motor.value
        duty = direction.value[index]

        if duty > 0:
            self.pwm.set_pwm(channel_a, 0, 0)
            self.pwm.set_pwm(channel_b, 0, duty)

        elif duty < 0:
            self.pwm.set_pwm(channel_a, 0, abs(duty))
            self.pwm.set_pwm(channel_b, 0, 0)

        else:
            self.pwm.set_pwm(channel_a, 0, 4095)
            self.pwm.set_pwm(channel_b, 0, 4095)

    def move(self, direction: Powertrain.Direction):
        log.debug(f"Moving motors in direction {direction}")
        self.set_motor(self.Motor.TopLeft, direction)
        self.set_motor(self.Motor.TopRight, direction)
        self.set_motor(self.Motor.BottomRight, direction)
        self.set_motor(self.Motor.BottomLeft, direction)


class VirtualPowertrain(Powertrain):
    orientation: str = "north"

    def move(self, direction):
        # direction pot ser una tupla de dos enters (si es fa forward o back) o un string (si es fa left o right)

        if isinstance(direction, tuple) and len(direction) == 2 and all(isinstance(i, int) for i in direction):
            log.debug(
                f"Moving vehicle adding {direction} to current coordinates")
            x_movement, y_movement = direction
            x_actual, y_actual = VirtualLocation.get()
            VirtualLocation.set(x_actual+x_movement, y_actual+y_movement)
        elif isinstance(direction, str):
            log.debug(f"Turning {direction}")
            self.orientation = direction
        else:
            log.error("Invalid direction type: {direction}")

    def get_orientation(self):
        return self.orientation
