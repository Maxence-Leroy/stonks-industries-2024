from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Optional

from src.constants import Side, PLAYING_AREA_WIDTH


class Location(ABC):
    """Abstract class for a location. Has a method `getLocation` that will be called when the move location is starting"""

    @abstractmethod
    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        raise NotImplementedError()

@dataclass
class AbsoluteCoordinates(Location):
    """Location with absolute coordinates which doesn't depend on the side"""

    def __init__(self, x: float, y: float, theta: float) -> None:
        """
        Parameters
        ----------
        x: float
            X position in mm

        y: float
            Y position in mm

        theta: float
            Angle in radians
        """

        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self) -> str:
        return f"Absolute (x: {self.x}, y: {self.y}, θ: {self.theta})"

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        return (self.x, self.y, self.theta)

@dataclass
class SideRelatedCoordinates(Location):
    """Location with "absolute" coordinates. They will be converted according to the side of the playing area."""

    def __init__(self, x: float, y: float, theta: float, side: Side) -> None:
        """
        Parameters
        ----------
        x: float
            X position in mm

        y: float
            Y position in mm

        theta: float
            Angle of the robot in radians
        
        side: Side
            Side of the robot
        """

        super().__init__()
        if side == Side.BLUE:
            self.x = x
            self.y = y
            self.theta = theta
        else:
            self.x = PLAYING_AREA_WIDTH - x
            self.y = y
            if 0 <= theta <= math.pi:
                self.theta = math.pi - theta
            else:
                self.theta = -math.pi - theta

    def __str__(self) -> str:
        return f"Side related (x: {self.x}, y: {self.y}, θ: {self.theta})"

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
    
