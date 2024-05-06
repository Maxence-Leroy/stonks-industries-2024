from abc import ABC, abstractmethod
from enum import Enum
from math import floor, ceil, fabs, sqrt
import numpy as np
from nptyping import NDArray, Bool, Shape
from typing import Self

from src.constants import ROBOT_DEPTH, ROBOT_WIDTH, PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH, D_STAR_FACTOR


def add(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] + b[0], a[1] + b[1])

def sub (a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] - b[0], a[1] - b[1])

def dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]

def hypot2(a: tuple[float, float], b: tuple[float, float]) -> float:
    return dot(sub(a, b), sub(a, b))

def proj(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    k = dot(a, b) / dot(b, b)
    return (k * b[0], k * b[1])

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

    @abstractmethod  
    def intersect_with_line(self, a: tuple[float, float], b: tuple[float, float]) -> bool:
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
        robot_max_dimension = max(ROBOT_DEPTH, ROBOT_WIDTH) / 2
        return Rectangle(
            max(0, self._x_min - robot_max_dimension),
            max(0, self._y_min - robot_max_dimension),
            min(PLAYING_AREA_WIDTH, self._x_max + robot_max_dimension),
            min(PLAYING_AREA_DEPTH, self._y_max + robot_max_dimension)
        )
    
    def center(self) -> tuple[float, float]:
        return ((self._x_min + self._x_max) / 2, (self._y_min + self._y_max) / 2)
    
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
    
    def intersect_with_line(self, a: tuple[float, float], b: tuple[float, float]) -> bool:
        return super().intersect_with_line(a, b) # TODO
    
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
    
    def distance_segment_to_point(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        # https://stackoverflow.com/a/1079478
        c = (self.x_center, self.y_center)
        
        # Compute vectors AC and AB
        ac = sub(c, a)
        ab = sub(b,a)

        # Get point D by taking the projection of AC onto AB then adding the offset of A
        d = add(proj(ac, ab), a)

        ad = sub(d, a)
        # D might not be on AB so calculate k of D down AB (aka solve AD = k * AB)
        # We can use either component, but choose larger value to reduce the chance of dividing by zero
        k = ad[0] / ab[0] if fabs(ab[0]) > fabs(ab[1]) else ad[1] / ab[1]

        # Check if D is off either end of the line segment
        if k <= 0.0:
            return sqrt(hypot2(c, a))
        elif (k >= 1.0):
            return sqrt(hypot2(c, b))
        else:
            return sqrt(hypot2(c, d))
    
    def intersect_with_line(self, a: tuple[float, float], b: tuple[float, float]) -> bool:
        return self.distance_segment_to_point(a, b) <= self._radius

