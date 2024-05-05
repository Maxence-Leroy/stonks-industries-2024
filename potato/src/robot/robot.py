import asyncio
from enum import Enum
import math
import numpy as np
import threading
import time
from typing import Self, Optional

from src.constants import MATCH_TIME, D_STAR_FACTOR, PLAYING_AREA_WIDTH, PLAYING_AREA_DEPTH, Side, ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT
from src.d_star import DStarLight, State
from src.helpers.pairwise import pairwise
from src.playing_area import playing_area
from src.robot.robot_actuator import create_robot_binary_actuator
from src.robot.robot_stepper_motors import create_stepper_motors
from src.robot.robot_switch_reader import RobotSwitchReader
from src.robot.lidar import lidar, LidarDirection
from src.location.location import AbsoluteCoordinates, SideRelatedCoordinates
from src.logging import logging_debug, logging_info, logging_error
from src.path_smoother import smooth_path
from src.replay.base_classes import ReplayEvent, EventType
from src.replay.save_replay import log_replay
from src.screen import screen
from src.robot.sts3215 import STS3215

class RobotMovement(Enum):
    FINISH_MOVING = 0
    IS_MOVING_FORWARD = 1
    IS_MOVING_BACKWARD = 2
    WAITING_LIDAR_FORWARD = 3
    WAITING_LIDAR_BACKWARD = 4
    WAITING_RECOMPUTE = 4

    def stop_because_of_lidar(self) -> Self:
        if self == RobotMovement.IS_MOVING_FORWARD:
            return RobotMovement.WAITING_LIDAR_FORWARD
        elif self == RobotMovement.IS_MOVING_BACKWARD:
            return RobotMovement.WAITING_LIDAR_BACKWARD
        else:
            raise ValueError()

    def restart_after_lidar(self) -> Self:
        if self == RobotMovement.WAITING_LIDAR_FORWARD:
            return RobotMovement.IS_MOVING_FORWARD
        elif self == RobotMovement.WAITING_LIDAR_BACKWARD:
            return RobotMovement.IS_MOVING_BACKWARD
        else:
            raise ValueError()
    
    def to_lidar_direction(self) -> Optional[LidarDirection]:
        if self == RobotMovement.WAITING_LIDAR_FORWARD or self == RobotMovement.IS_MOVING_FORWARD:
            return LidarDirection.FORWARD
        elif self == RobotMovement.WAITING_LIDAR_BACKWARD or self == RobotMovement.IS_MOVING_BACKWARD:
            return LidarDirection.BACKWARD
        else:
            return None
        
    def is_moving(self) -> bool:
        return self == RobotMovement.IS_MOVING_BACKWARD or self == RobotMovement.IS_MOVING_FORWARD

    def is_waiting_lidar(self) -> bool:
        return self == RobotMovement.WAITING_LIDAR_BACKWARD or self == RobotMovement.WAITING_LIDAR_FORWARD  

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
    robot_movement: RobotMovement
    current_location: AbsoluteCoordinates
    last_instruction: str
    servo_ids: list[int]

    def __init__(self) -> None:
        self.stepper_motors = create_stepper_motors()

        self.current_location = AbsoluteCoordinates(0, 0, 0)
        self.score = 0
        self.servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT]

        self.sts3215 = STS3215()

        self.start_switch = RobotSwitchReader(
            chip="gpiochip1", line=97, name="Start switch"
        )

        self.side_switch = RobotSwitchReader(
            chip="gpiochip1", line=96, name="Side switch"
        )

        self.robot_movement = RobotMovement.FINISH_MOVING
        self.start_time = 0

        self.led_ethernet = create_robot_binary_actuator(
            chip="gpiochip1", line=15, name="Ethernet LED"
        )

        self.magnet1 = create_robot_binary_actuator(
            chip="gpiochip1", line=81, name="Magnet 1"
        )

        self.magnet2 = create_robot_binary_actuator(
            chip="gpiochip1", line=82, name="Magnet 2"
        )

        self.magnet3 = create_robot_binary_actuator(
            chip="gpiochip1", line=83, name="Magnet 3"
        )

        self.last_instruction = ""

        # Always read the serial from stepper motors to update the robot's state
        thread_read_serial = threading.Thread(target=self.read_serial)
        thread_read_serial.start()

        # Always have lidar scannong
        thread_lidar = threading.Thread(target=self.handle_lidar)
        thread_lidar.start()

        thread_screen = threading.Thread(target=self.update_screen)
        thread_screen.start()

    def wait_to_start(self):
        """
        Function to set up the side and position of the robot before the start of the game.
        Returns when the start switch changes its value
        """
        while self.start_switch.get_value() is False:
            time.sleep(0.1)
            if self.side_switch.get_value() is True and playing_area.side is Side.BLUE:
                playing_area.side = Side.YELLOW
                self.set_initial_position(SideRelatedCoordinates(0, 0, 0, playing_area.side))
                logging_info("Yellow side")
                screen.show_robot_name_and_side(playing_area.side)
            elif self.side_switch.get_value() is False and playing_area.side is Side.YELLOW:
                playing_area.side = Side.BLUE
                self.set_initial_position(SideRelatedCoordinates(0, 0, 0, playing_area.side))
                logging_info("Blue side")
                screen.show_robot_name_and_side(playing_area.side)

    def update_screen(self):
        """Fonction to update the content of the I2C screen with time and score"""
        previous_score = 0
        previous_time = 0

        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME + 5:
            if self.start_time == 0:
                time.sleep(1)
                continue
            
            current_time = self.get_current_time()
            if int(current_time) != int(previous_time) or previous_score != self.score:
                previous_score = self.score
                previous_time = current_time
                
                try:
                    screen.show_time_score(min(MATCH_TIME, current_time), self.score)
                except Exception as ex:
                    logging_error(f"Error with screen: {ex}")
            
            time.sleep(0.5)

    def get_current_time(self) -> float:
        """Get current time on the match (normally between 0 and 100)"""
        return time.time() - self.start_time

    def handle_lidar(self):
        """Handle lidar and stop when needed"""
        safety_distance = 250
        cone_angle = math.pi / 3

        last_replay_log = 0
        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME:
            current_time = self.get_current_time()
            if current_time > 0:
                direction = self.robot_movement.to_lidar_direction()
                if direction is None:
                    time.sleep(0.1)
                    continue

                location = self.current_location.getLocation(0, 0, 0)
                if location is None:
                    raise ValueError()
                (x, y, theta) = location
                points_with_angle = lidar.scan_points()
                points_with_coordinates = lidar.get_lidar_coordinates(points_with_angle, x, y, theta)
                field_filter = lidar.filter_on_field(points_with_coordinates)
                points_with_angle = points_with_angle[field_filter, :] if len(field_filter) > 0 else points_with_angle
                points_with_coordinates = points_with_coordinates[field_filter, :] if len(field_filter) > 0 else points_with_coordinates
                direction_filter = lidar.filter_direction(points_with_angle, direction, cone_angle)
                points_with_angle = points_with_angle[direction_filter, :] if len(direction_filter) > 0 else points_with_angle
                points_with_coordinates = points_with_coordinates[direction_filter, :] if len(direction_filter) > 0 else points_with_coordinates
                intensity_filter = points_with_coordinates[:, 2] > 200 if len(points_with_coordinates) > 0 else np.array([])

                if current_time - last_replay_log >= 1:
                    last_replay_log = current_time
                    if len(points_with_coordinates) > 0:
                        for point in points_with_coordinates[intensity_filter, :]:
                            log_replay(ReplayEvent(EventType.LIDAR, (point[0], point[1], 0), point[2], current_time))

                if self.robot_movement.is_moving():
                    if len(points_with_angle) > 0:
                        minimum_distance = np.min(points_with_angle[:,1])
                    else:
                        minimum_distance = np.inf
                    logging_debug(f"Lidar minimum distance is {minimum_distance}")
                    if minimum_distance < safety_distance:
                        self.stop_moving(self.robot_movement.stop_because_of_lidar())
                        logging_info(f"Stopping due to close object: {minimum_distance}")

                elif self.robot_movement.is_waiting_lidar():
                    if len(points_with_angle) > 0:
                        minimum_distance = np.min(points_with_angle[:,1])
                    else:
                        minimum_distance = np.inf
                    if minimum_distance > safety_distance:
                        self.stop_moving(self.robot_movement.restart_after_lidar())
                        self.stepper_motors.write(self.last_instruction)
                        logging_info(f"Restarting since object is gone: {minimum_distance}")

                time.sleep(0.1)

    def read_serial(self):
        """Read the serail from stepper motors. Will stop at the end of the match"""
        while self.start_time == 0 or self.get_current_time() <= MATCH_TIME:
            res = self.stepper_motors.read()
            logging_debug(f"Serial recieved {res}")
            if res == "":
                # Proably timeout
                pass
            elif res == "DONE":
                self.robot_movement = RobotMovement.FINISH_MOVING
            else:
                res = res[1:-1] # Remove parenthesis
                coordinates = res.split(";")
                try:
                    x = float(coordinates[0])
                    y = float(coordinates[1])
                    theta = float(coordinates[2])
                    logging_debug(f"Current robot position {x},{y},{theta}")
                    log_replay(
                        ReplayEvent(
                            event=EventType.ROBOT_POSITION,
                            place=(x, y, theta)
                        )
                    )
                    self.current_location = AbsoluteCoordinates(x, y, theta)
                except Exception as ex:
                    logging_error(f"Exception while parsing robot: {ex}")
                    logging_error(f"With input {res}")

    def set_initial_position(self, location: SideRelatedCoordinates) -> None:
        absolute_position = location.getLocation(0, 0, 0)
        if absolute_position != None:
            (x, y, theta) = absolute_position
            self.current_location = AbsoluteCoordinates(x, y, theta)
        log_replay(
            ReplayEvent(
                event=EventType.ROBOT_POSITION,
                place=(location.x, location.y, location.theta)
            )
        )
        self.stepper_motors.write(f"INIT ({location.x};{location.y};{location.theta})\n")

    def stop_moving(self, cause: RobotMovement):
        """Function to be called when a move action timeout
        (will normally be automaticly done at the end of the match)

        Parameters
        ----------
        cause: RobotMovement
           Cause of the stop (timeout, lidar or path calculation)
        """
        instruction = "STOP\n"
        self.stepper_motors.write(instruction)
        self.robot_movement = cause

    def send_d_star_path(self, path: list[tuple[float, float]], x: float, y: float, theta: float, backwards: bool, forced_angle: bool):
        logging_debug(str(path))
        instruction = ""
        smoothed_path = smooth_path(path) if len(path) > 1 else path
        for point in smoothed_path:
            log_replay(
                ReplayEvent(
                    event=EventType.ROBOT_PATHING,
                    place=(point[0]*D_STAR_FACTOR, point[1] * D_STAR_FACTOR, 0)
                )
            )
            if instruction != "":
                instruction += ","
            instruction += f"({round(point[0]*D_STAR_FACTOR, 2)};{round(point[1]*D_STAR_FACTOR, 2)};{0};{'1' if backwards else '0'};0)"

            instruction += f",({x};{y};{theta};{'1' if backwards else '0'};{'1' if forced_angle else '0'})\n"
            self.last_instruction = instruction
            self.stepper_motors.write(instruction)
            self.robot_movement = RobotMovement.IS_MOVING_BACKWARD if backwards else RobotMovement.IS_MOVING_FORWARD

    async def go_to(
        self, x: float, y: float, theta: float, backwards: bool, forced_angle: bool, on_the_spot: bool, max_speed: int, max_acceleration: int, precision: int
    ) -> None:
        """Function to move to specific coordinates. Returns when the Arduino has sent "DONE"."""
        log_replay(
            ReplayEvent(
                event=EventType.ROBOT_DESTINATION,
                place=(x, y, theta)
            )
        )
        instruction = f"({x};{y};{theta};{'1' if backwards else '0'};{'1' if forced_angle else '0'};{'1' if on_the_spot else '0'};{max_speed};{max_acceleration};{'1' if precision else '0'})\n"
        self.last_instruction = instruction
        self.robot_movement = RobotMovement.IS_MOVING_BACKWARD if backwards else RobotMovement.IS_MOVING_FORWARD
        self.stepper_motors.write(instruction)
        while self.robot_movement != RobotMovement.FINISH_MOVING: #type: ignore
            await asyncio.sleep(0.2)
        return


robot = Robot() # Singleton