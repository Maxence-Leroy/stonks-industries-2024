from typing import Optional
import gpiod

class RobotSwitchReader():
    """Read the state of a switch"""
    def __init__(self, chip: str, line: int, name: Optional[str]) -> None:
        self.name = name or f"{chip} line {line}"
        self.chip = gpiod.chip(chip)
        self.line = self.chip.get_line(line)
        self.config = gpiod.line_request()
        self.config.consumer = "Application" #I don't know what are the possible values
        self.config.request_type = gpiod.line_request.DIRECTION_INPUT
        self.config.flags = gpiod.line_request.FLAG_BIAS_PULL_DOWN
        self.line.request(self.config)

    def __str__(self) -> str:
        return self.name

    def get_value(self) -> bool:
        """Return true if the switch is on"""
        return self.line.get_value() == 1
