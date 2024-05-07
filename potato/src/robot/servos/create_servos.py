import serial
from typing import Tuple

from src.constants import mock_robot
from src.robot.servos.sts3215 import STS3215, MockSTS3215
from src.robot.servos.scs0009 import SCS0009, MockSCS0009

def create_servos() -> Tuple[STS3215, SCS0009]:
    if mock_robot:
        return(MockSTS3215(), MockSCS0009())
    else:
        servo_serial = serial.Serial(
            port="/dev/ttyAML7",
            baudrate=1000000,
            timeout=10,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        return (STS3215(servo_serial), SCS0009(servo_serial))