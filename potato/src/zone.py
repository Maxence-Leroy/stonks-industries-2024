from abc import ABC, abstractmethod
from enum import Enum
from math import floor, ceil, sqrt, pow
from typing import Self

from src.constants import ROBOT_DEPTH, ROBOT_WIDTH, PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH

class Zone(ABC):
    @abstractmethod
    def zone_with_robot_size(self) -> Self:
        raise NotImplementedError()
    
    @abstractmethod
    def points_in_zone(self) -> list[tuple[int, int]]:
        raise NotImplementedError()
    
    class Rounding(Enum):
        Minimum = 0
        Maximum = 1
        
    def int_coordinates(self, coordinate: float, side: Rounding) -> int:
        if int(coordinate) == coordinate:
            return int(coordinate)
        elif side == Zone.Rounding.Minimum:
            return floor(coordinate)
        else:
            return ceil(coordinate)

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
    
    def points_in_zone(self) -> list[tuple[int, int]]:
        points: list[tuple[int, int]] = []
        for x in range(int(self.int_coordinates(self._x_min, Zone.Rounding.Minimum)/ 10), int(self.int_coordinates(self._x_max, Zone.Rounding.Maximum) / 10) + 1):
            for y in range(int(self.int_coordinates(self._y_min, Zone.Rounding.Minimum)/ 10), int(self.int_coordinates(self._y_max, Zone.Rounding.Maximum) / 10) + 1):
                points.append((x, y))
        return points
    
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
    
    def points_in_zone(self) -> list[tuple[int, int]]:
        points: list[tuple[int, int]] = []
        x_min = self.int_coordinates(max(0, self._x_center - self._radius), Zone.Rounding.Minimum) / 10
        y_min = self.int_coordinates(max(0, self._y_center - self._radius), Zone.Rounding.Minimum) / 10
        x_max = self.int_coordinates(min(PLAYING_AREA_WIDTH, self._x_center + self._radius), Zone.Rounding.Maximum) / 10
        y_max = self.int_coordinates(min(PLAYING_AREA_DEPTH, self._y_center + self._radius), Zone.Rounding.Maximum) / 10

        for x in range(int(x_min), int(x_max + 1)):
            for y in range(int(y_min), int(y_max + 1)):
                if (sqrt(pow(x * 10 - self._x_center, 2) + pow(y * 10 - self._y_center, 2)) < self._radius):
                    points.append((x, y))

        return points