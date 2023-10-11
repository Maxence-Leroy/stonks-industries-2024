import asyncio
import serial
import threading
import time

from src.constants import MATCH_TIME
from src.robot_actuator import RobotBinaryActuator
from src.location import Coordinates
from src.logging import logging_debug
class Robot:
    start_time: float
    is_moving: bool
    current_location: Coordinates

    def __init__(self) -> None:
        self.stepper_motors = serial.Serial(
            port="/dev/ttyAML6",
            baudrate=115200,
            timeout=MATCH_TIME,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            write_timeout=1.0,
        )

        self.is_moving = False
        self.start_time = 0

        self.led_ethernet = RobotBinaryActuator(
            chip="gpiochip1", line=15, name="Ethernet LED"
        )

        thread = threading.Thread(target=self.read_serial)
        thread.start()

    def get_current_time(self) -> float:
        return time.time() - self.start_time

    def read_serial(self):
        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME:
            res = self.stepper_motors.read_until(b"\n").decode()
            res = res.strip("\n")
            logging_debug(res)
            if res == "":
                # Proably timeout
                pass
            elif res == "DONE":
                self.is_moving = False
            else:
                res = res[1:-1] # Remove parenthesis
                coordinates = res.split(";")
                x = float(coordinates[0])
                y = float(coordinates[1])
                theta = float(coordinates[2])
                logging_debug(f"Current robot position {x},{y},{theta}")
                self.current_location = Coordinates(x, y, theta)

    def stop_moving(self):
        instruction = "STOP\n"
        self.stepper_motors.write(instruction.encode("utf-8"))
        self.is_moving = False
        self.stepper_motors.flush()

    async def go_to(
        self, x: float, y: float, theta: float, timer_limit: float | None
    ) -> None:
        instruction = f"({x};{y};{theta})\n"
        self.stepper_motors.write(instruction.encode("utf-8"))
        self.stepper_motors.flush()
        self.is_moving = True
        while self.is_moving:
            await asyncio.sleep(0.2)
        return
