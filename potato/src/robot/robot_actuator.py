from abc import ABC, abstractmethod
from typing import Optional
import gpiod

from src.constants import mock_robot
from src.logging import logging_debug

class RobotBinaryActuator(ABC):
    """Class representing a binary actuator of the robot: its value can be either 0 or 1"""
    def __init__(self, chip: str, line: int, name: Optional[str]) -> None:
        self.name = name or f"{chip} line {line}"

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def switch_on(self) -> None:
        """Switch on the actuator (value: 1)"""
        raise NotImplementedError()

    @abstractmethod
    def switch_off(self) -> None:
        """Switch off the actuator (value: 0)"""
        raise NotImplementedError()
    

class RealRobotBinaryActuator(RobotBinaryActuator):
    """Real implementation"""
    def __init__(self, chip: str, line: int, name: Optional[str]) -> None:
        super().__init__(chip, line, name)
        self.chip = gpiod.chip(chip)
        self.line = self.chip.get_line(line)
        self.config = gpiod.line_request()
        self.config.consumer = "Application" #I don't know what are the possible values
        self.config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.line.request(self.config)

    def switch_on(self):
        self.line.set_value(1)

    def switch_off(self):
        self.line.set_value(0)

class MockRobotBinaryActuator(RobotBinaryActuator):
    """Mock implementation"""
    def __init__(self, chip: str, line: int, name: Optional[str]) -> None:
        super().__init__(chip, line, name)

    def switch_on(self) -> None:
        logging_debug(f"Mock actuator: Switch on {self}")
        
    def switch_off(self) -> None:
        logging_debug(f"Mock actuator: Switch off {self}")

def create_robot_binary_actuator(chip: str, line: int, name: Optional[str] = None) -> RobotBinaryActuator:
        """
        Parameters
        ----------
        chip: string
            Name of the chip where the actuator is plugged (usually "gpiochip0" or "gpiochip1")

        line: int
            Index of the line where the actuator is plugged '(usually between 0 and 100)

        name: Optional[str]
            Name of the actuator (only used for debug). 
            If not provided, it will be the name of the chip and the number of the line
        """
        if mock_robot:
            return MockRobotBinaryActuator(chip, line, name)
        else:
            return RealRobotBinaryActuator(chip, line, name)