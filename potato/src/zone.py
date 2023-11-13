from abc import ABC, abstractmethod
from typing import Self

from src.constants import ROBOT_DEPTH, ROBOT_WIDTH, PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH

class Zone(ABC):
    @abstractmethod
    def zone_with_robot_size(self) -> Self:
        raise NotImplementedError()

class Rectangle(Zone):
    _x_min: float
    _x_max: float
    _y_min: float
    _y_max: float

    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float) -> None:
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max

    def zone_with_robot_size(self) -> Self:
        robot_max_dimension = max(ROBOT_DEPTH, ROBOT_WIDTH)
        return Rectangle(
            max(0, self._x_min - robot_max_dimension),
            max(0, self._y_min - robot_max_dimension),
            min(PLAYING_AREA_WIDTH, self._x_max + robot_max_dimension),
            min(PLAYING_AREA_DEPTH, self._y_max + robot_max_dimension)
        )
    
class Circle(Zone):
    _x_center: float
    _y_center: float
    _radius: float

    def __init__(self, x_center: float, y_center: float, radius: float) -> None:
        self._x_center = x_center
        self._y_center = y_center
        self._radius = radius

    def zone_with_robot_size(self) -> Self:
        robot_max_dimension = max(ROBOT_DEPTH, ROBOT_WIDTH)
        return Circle(self._x_center, self._y_center, self._radius + robot_max_dimension)