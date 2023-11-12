import asyncio
from math import fabs, pi
from queue import Queue
import threading
import time
from typing import Optional

from src.constants import MATCH_TIME
from src.robot_actuator import create_robot_binary_actuator
from src.robot_stepper_motors import create_stepper_motors
from src.location import Coordinates
from src.path.angle import Angle
from src.path.path import Path
from src.path.line import Line
from src.path.rotation import Rotation
from src.logging import logging_debug
class Robot:
    """
    Class reprensatation of the robot
    TODO: Add state

    Attributes
    ----------
    start_time: float
        Time value when the match has begun
    
    is_moving: bool
        Whever the stepper motors are currently working

    current_location: Coordinates
        Current location of the robot. 
        The coordinates will be converted depending on the side of the playing area.

    stepper_motors: RobotStepperMotors
        Object reprensenting the stepper mottors. Either a real one (with UART to Arduino) or a mock

    led_ethernet: RobotBinaryActuator
        Mock up of a binary actuator of the robot.
        All the actuators will be attributes of the class
    """
    start_time: float
    is_moving: bool
    current_location: Coordinates
    aimed_position: Coordinates
    path_queue: Queue[Path]
    current_path: Optional[Path]

    def __init__(self) -> None:
        self.stepper_motors = create_stepper_motors()

        self.path_queue = Queue(maxsize=0)

        self.is_moving = False
        self.start_time = 0

        self.current_path = None

        self.led_ethernet = create_robot_binary_actuator(
            chip="gpiochip1", line=15, name="Ethernet LED"
        )

        # Always read the serial from stepper motors to update the robot's state
        receive_thread = threading.Thread(target=self.read_serial)
        receive_thread.start()

        move_thread = threading.Thread(target=self.enslave)
        move_thread.start()

    def get_current_time(self) -> float:
        """Get current time on the match (normally between 0 and 100)"""
        return time.time() - self.start_time
    
    def set_initial_position(self, coordinates: Coordinates) -> None:
        self.current_location = coordinates
        self.stepper_motors.write(f"INIT ({coordinates.x};{coordinates.y};{coordinates.theta.to_float()})\n")

    def read_serial(self):
        """Read the serail from stepper motors. Will stop at the end of the match"""
        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME:
            res = self.stepper_motors.read()
            logging_debug(f"Serial recieved {res}")
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
                self.current_location = Coordinates(x, y, Angle(theta))

    def stop_moving(self):
        """Function to be called when a move action timeout
        (will normally be automaticly done at the end of the match)
        """
        # Empty the queue
        while not self.path_queue.empty():
            self.path_queue.get_nowait()
        
        instruction = "STOP\n"
        self.stepper_motors.write(instruction)
        self.is_moving = False

    async def go_to(
        self, x: float, y: float, theta: Angle, backwards: bool
    ) -> None:
        """Function to move to specific coordinates. Returns when the Arduino has sent "DONE"."""

        current_x = self.current_location.x
        current_y = self.current_location.y
        current_theta = self.current_location.theta
        required_theta = current_theta

        if fabs(x - current_x) > 0.5 or fabs(y - current_y) > 0.05:
            required_theta = Angle.compute_angle(current_x, current_y, x, y)
            if backwards:
                current_theta += pi

            if fabs((required_theta - current_theta).to_float()) > 0.1:
                self.path_queue.put_nowait(Rotation(current_x, current_y, current_theta, required_theta))

            self.path_queue.put_nowait(Line(current_x, current_y, x, y, backwards))

            if backwards:
                current_theta -= pi

        if fabs((current_theta - theta).to_float()) > 0.05:
            self.path_queue.put_nowait(Rotation(x, y, required_theta, theta))

        self.is_moving = True
        while self.is_moving:
            await asyncio.sleep(0.2)
        return
    
    def enslave(self):
        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME:
            if self.current_path is not None:
                expected_coordinates = self.current_path.expected_position(time.time())
                instruction = f"({expected_coordinates.x};{expected_coordinates.y};{expected_coordinates.theta.to_float()};{"1" if self.current_path.is_going_backwards() else "0"})\n"
                self.stepper_motors.write(instruction)
                if self.current_path.is_over():
                    self.current_path = None
            elif not self.path_queue.empty():
                self.current_path = self.path_queue.get_nowait()
                self.current_path.start()
            else:
                self.is_moving = False
                time.sleep(0.1)


robot = Robot() # Singleton