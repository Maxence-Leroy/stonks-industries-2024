from abc import ABC, abstractmethod
import serial

from src.constants import MATCH_TIME, mock_robot
from src.logging import logging_debug, logging_error

class RobotStepperMotors(ABC):
    """Abstract class to define stepper motors actions"""
  
    @abstractmethod
    def write(self, text: str) -> None:
        """Send text to the serial"""
        raise NotImplementedError()
    
    @abstractmethod
    def read(self) -> str:
        """Read text from the serial"""
        raise NotImplementedError()

class SerialStepperMotors(RobotStepperMotors):
    """Real class for stepper motors"""

    def __init__(self) -> None:
        self.serial = serial.Serial(
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

    def write(self, text: str) -> None:
        self.serial.write(text.encode("utf-8"))
        self.serial.flush()

    def read(self) -> str:
        try:
            res = self.serial.read_until(b"\n").decode()
            res = res.strip("\n")
            return res
        except Exception as ex:
            logging_error("Parse error")
            return ""

class MockStepperMotors(RobotStepperMotors):
    """Mock class for stepper motors. To be used when executing the strategy without the potato computer"""
    def write(self, text: str) -> None:
        logging_debug(f"Mock serial {text}")

    def read(self) -> str:
        res = input("serial input: ")
        return res

def create_stepper_motors() -> RobotStepperMotors:
    if mock_robot:
        return MockStepperMotors()
    else:
        return SerialStepperMotors()