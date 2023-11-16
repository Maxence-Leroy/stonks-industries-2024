from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Optional


class Location(ABC):
    """Abstract class for a location. Has a method `getLocation` that will be called when the move location is starting"""

    @abstractmethod
    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        raise NotImplementedError()

@dataclass
class Coordinates(Location):
    """Location with "absolute" coordinates. They will be converted according to the side of the playing area."""

    def __init__(self, x: float, y: float, theta: float) -> None:
        """
        Parameters
        ----------
        x: float
            X position in mm

        y: float
            Y position in mm

        theta: float
            Angle of the robot in radians
        """

        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y}, θ: {self.theta})"

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        return (self.x, self.y, self.theta)

class RelativeMove(Location):
    """Location with "relative" coordinates. They will be converted according to the side of the playing area."""

    def __init__(self, x: float, y: float, theta: float) -> None:
        """
        Parameters
        ----------
        x: float
            X position in mm

        y: float
            Y position in mm

        theta: float
            Angle of the robot in radians
        """

        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y}, θ: {self.theta})"

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        return (current_x + self.x, current_y + self.y, current_theta + self.theta)
    
class MoveForward(Location):
    """Move forward depending on the direction the robot is facing."""

    def __init__(self, distance: float) -> None:
        """
        Parameters
        ----------
        distance: float
            distance in mm
        """

        super().__init__()
        self.distance = distance

    def __str__(self) -> str:
        return f"Distance {self.distance}"

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        return (current_x + self.distance * math.cos(current_theta), current_y + self.distance * math.sin(current_theta), current_theta)
    
