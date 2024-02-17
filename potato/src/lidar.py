from typing import Optional
import numpy as np
import ydlidar

from src.logging import logging_error

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

    def scan_points(self):
        if self.scan is not None:
            r = self.laser.doProcessSimple(self.scan)
            if r:
                numpy_points = np.array([[p.angle, p.range if p.range > 0 else np.inf, p.intensity] for p in self.scan.points])
                return numpy_points
            else:
                logging_error("Unable to read lidar")
                return np.array([])

lidar = Lidar() # Singleton