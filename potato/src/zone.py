from abc import ABC, abstractmethod
from enum import Enum
from math import floor, ceil
import numpy as np
from nptyping import NDArray, Bool, Shape
from typing import Self

from src.constants import ROBOT_DEPTH, ROBOT_WIDTH, PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH, D_STAR_FACTOR

class Zone(ABC):
    @abstractmethod
    def zone_with_robot_size(self) -> Self:
        raise NotImplementedError()
    
    @abstractmethod
    def points_in_zone(self) -> NDArray[Shape["300,200"], Bool]:
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
        robot_max_dimension = max(ROBOT_DEPTH, ROBOT_WIDTH) / 2
        return Rectangle(
            max(0, self._x_min - robot_max_dimension),
            max(0, self._y_min - robot_max_dimension),
            min(PLAYING_AREA_WIDTH, self._x_max + robot_max_dimension),
            min(PLAYING_AREA_DEPTH, self._y_max + robot_max_dimension)
        )
    
    def points_in_zone(self) -> NDArray[Shape["60,40"], Bool]:
        array = np.full((int(PLAYING_AREA_WIDTH / D_STAR_FACTOR), int(PLAYING_AREA_DEPTH / D_STAR_FACTOR)), False)
        x_min = self.int_coordinates(self._x_min / D_STAR_FACTOR, Zone.Rounding.Minimum)
        x_max = self.int_coordinates(self._x_max / D_STAR_FACTOR, Zone.Rounding.Maximum)
        y_min = self.int_coordinates(self._y_min / D_STAR_FACTOR, Zone.Rounding.Minimum)
        y_max = self.int_coordinates(self._y_max / D_STAR_FACTOR, Zone.Rounding.Maximum)
        array[x_min:x_max+1, y_min:y_max+1] = True
        return array
    
    def __str__(self) -> str:
        return f"Rectangle ({self._x_min},{self._y_min}) -> ({self._x_max, self._y_max})"
    
class Circle(Zone):
    x_center: float
    y_center: float
    _radius: float

    def __init__(self, x_center: float, y_center: float, radius: float) -> None:
        self.x_center = x_center
        self.y_center = y_center
        self._radius = radius

    def zone_with_robot_size(self) -> Self:
        robot_max_dimension = max(ROBOT_DEPTH, ROBOT_WIDTH) / 2
        return Circle(self.x_center, self.y_center, self._radius + robot_max_dimension)
    
    def points_in_zone(self) -> NDArray[Shape["60,40"], Bool]:
        x_center = int(self.x_center / D_STAR_FACTOR)
        y_center = int(self.y_center / D_STAR_FACTOR)
        radius = self._radius / D_STAR_FACTOR
        width = int(PLAYING_AREA_WIDTH / D_STAR_FACTOR)
        height = int(PLAYING_AREA_DEPTH / D_STAR_FACTOR)
        X, Y = np.ogrid[:width, :height]
        dist_from_center = np.sqrt((X-x_center)**2 + (Y-y_center)**2)
        mask = np.ceil(dist_from_center) <= radius
        return mask
    
    def __str__(self) -> str:
        return f"Circle center({self.x_center},{self.y_center}) radius {self._radius}"
