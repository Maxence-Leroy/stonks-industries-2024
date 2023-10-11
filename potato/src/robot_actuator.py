from typing import Optional
import gpiod


class RobotBinaryActuator:
    """Class representing a binary actuator of the robot: its value can be either 0 or 1"""

    def __init__(self, chip: str, line: int, name: Optional[str] = None) -> None:
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

        self.chip = gpiod.chip(chip)
        self.line = self.chip.get_line(line)
        self.name = name or f"{chip} line {line}"
        self.config = gpiod.line_request()
        self.config.consumer = "Application" #I don't know what are the possible values
        self.config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.line.request(self.config)

    def __str__(self) -> str:
        return self.name

    def switch_on(self):
        """Switch on the actuator (value: 1)"""

        self.line.set_value(1)

    def switch_off(self):
        """Switch off the actuator (value: 0)"""
        self.line.set_value(0)
