import numpy as np
import ydlidar
import time

if __name__ == "__main__":
    ydlidar.os_init()
    port = "/dev/ttyUSB0"
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 6.0)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
    laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 12.0)
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.12)
    laser.setlidaropt(ydlidar.LidarPropIntenstiy, True)

    ret = laser.initialize()
    if ret:
        ret = laser.turnOn()
        scan = ydlidar.LaserScan()
        while ret and ydlidar.os_isOk() :
            r = laser.doProcessSimple(scan)
            if r:
               numpy_points = np.array([[p.angle, p.range if p.range > 0 else np.inf, p.intensity] for p in scan.points])
               print(np.min(numpy_points[:, 1]))
            else :
                print("Failed to get Lidar Data")
            print("")
            time.sleep(0.1)
        laser.turnOff()
    laser.disconnecting()
