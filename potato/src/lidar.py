from enum import Enum
from typing import Optional
import math
from nptyping import NDArray, Float, Shape, Bool
import numpy as np
import ydlidar

from src.constants import PLAYING_AREA_WIDTH, PLAYING_AREA_DEPTH
from src.logging import logging_error

class LidarDirection(Enum):
    ALL = 0
    FORWARD = 1
    BACKWARD = 2

class Lidar:
    scan: Optional[ydlidar.LaserScan]

    def __init__(self):
        ydlidar.os_init()
        port = "/dev/ttyUSB0"
        self.laser = ydlidar.CYdLidar()
        self.laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
        self.laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
        self.laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
        self.laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        self.laser.setlidaropt(ydlidar.LidarPropScanFrequency, 12.0)
        self.laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)
        self.laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
        self.laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
        self.laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
        self.laser.setlidaropt(ydlidar.LidarPropMaxRange, 4.0)
        self.laser.setlidaropt(ydlidar.LidarPropMinRange, 0.12)
        self.laser.setlidaropt(ydlidar.LidarPropIntenstiy, True)

        ret = self.laser.initialize()
        if ret:
            ret = self.laser.turnOn()
            self.scan = ydlidar.LaserScan()
        else:
            logging_error("Unable to start lidar")
            self.laser.disconnecting()
            self.scan = None

    def get_lidar_coordinates(self, points_with_angle: NDArray[Shape["360, 3"], Float], robot_x: float, robot_y: float, robot_theta: float) -> NDArray[Shape["360, 3"], Float]:
        coordinates_of_detection: list[list[float]] = []
        for point in points_with_angle:
            coordinates_of_detection.append(
                [robot_x + point[1] * math.cos(robot_theta + point[0]), 
                 robot_y + point[1] * math.sin(robot_theta + point[0]),
                 point[2]]
            )

        return np.array(coordinates_of_detection)


    def filter_on_field(self, coordinates_of_detection: NDArray[Shape["360, 3"], Float]) -> NDArray[Shape["200, 1"], Bool]:
        return (coordinates_of_detection[:, 0] >= 0) & (coordinates_of_detection[:, 0] <= PLAYING_AREA_WIDTH) &  (coordinates_of_detection[:, 1] >= 0) & (coordinates_of_detection[:, 1] <= PLAYING_AREA_DEPTH)
    
    def filter_direction(self, points_with_angle: NDArray[Shape["360, 3"], Float], direction: LidarDirection, cone_angle: float) -> NDArray[Shape["200, 1"], Bool]:
        if direction == LidarDirection.FORWARD:
            return (-cone_angle <= points_with_angle[:, 0]) & (points_with_angle[:, 0] <= cone_angle)
        elif direction == LidarDirection.BACKWARD:
            return (points_with_angle[:, 0] <= -math.pi/2 - cone_angle) | (points_with_angle[:, 0] >= math.pi / 2 + cone_angle)
        else:
            raise ValueError()


    def scan_points(self) -> NDArray[Shape["360, 3"], Float]:
        if self.scan is not None:
            r = self.laser.doProcessSimple(self.scan)
            if r:
                numpy_points = np.array([[math.pi - p.angle if p.angle >= 0 else -math.pi - p.angle, p.range * 1000 if p.range > 0 else np.inf, p.intensity] for p in self.scan.points])
                return numpy_points
            else:
                logging_error("Unable to read lidar")
                return np.array([])
        else:
            return np.array([])

lidar = Lidar() # Singleton