from typing import Optional
import gpiod


class RobotBinaryActuator:
    def __init__(self, chip: str, line: int, name: Optional[str] = None) -> None:
        self.chip = gpiod.chip(chip)
        self.line = self.chip.get_line(line)
        self.name = name or f"{chip} line {line}"
        self.config = gpiod.line_request()
        self.config.consumer = "Application"
        self.config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.line.request(self.config)

    def __str__(self) -> str:
        return self.name

    def switch_on(self):
        self.line.set_value(1)

    def switch_off(self):
        self.line.set_value(0)
