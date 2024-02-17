from enum import Enum
from typing import Optional
import math
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
        self.laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
        self.laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)
        self.laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
        self.laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
        self.laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
        self.laser.setlidaropt(ydlidar.LidarPropMaxRange, 12.0)
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

    def scan_points(self, direction: LidarDirection, cone_angle: float, robot_x: float, robot_y: float, robot_theta: float):
        if self.scan is not None:
            r = self.laser.doProcessSimple(self.scan)
            if r:
                numpy_points = np.array([[math.pi - p.angle if p.angle >= 0 else -math.pi - p.angle, p.range * 1000 if p.range > 0 else np.inf, p.intensity] for p in self.scan.points])
                if direction == LidarDirection.FORWARD:
                    forward_angles = (-cone_angle <= numpy_points[:, 0]) & (numpy_points[:, 0] <= cone_angle)
                    numpy_points = numpy_points[forward_angles, :]
                elif direction == LidarDirection.BACKWARD:
                    backward_angles = (numpy_points[:, 0] <= -math.pi/2 - cone_angle) | (numpy_points[:, 0] >= math.pi / 2 + cone_angle)
                    numpy_points = numpy_points[backward_angles, :]

                coordinates_of_detection: list[list[float]] = []
                for point in numpy_points:
                    coordinates_of_detection.append(
                        [robot_x + point[1] * math.cos(robot_theta + point[0]), 
                         robot_y + point[1] * math.sin(robot_theta + point[0])]
                    )

                np_coordinates_of_detection = np.array(coordinates_of_detection)
                points_in_field = (np_coordinates_of_detection[:, 0] >= 0) & (np_coordinates_of_detection[:, 0] <= PLAYING_AREA_WIDTH) &  (np_coordinates_of_detection[:, 1] >= 0) & (np_coordinates_of_detection[:, 1] <= PLAYING_AREA_DEPTH)

                return numpy_points[points_in_field, :]
            else:
                logging_error("Unable to read lidar")
                return np.array([])

lidar = Lidar() # Singleton