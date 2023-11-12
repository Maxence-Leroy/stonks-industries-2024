from math import pi, fabs, atan
from typing import Self

class Angle:
    def __init__(self, angle: float):
        self._angle = angle
        self._adjust()

    def _adjust(self):
        while self._angle > pi:
            self._angle -= 2 * pi
        while self._angle < -pi:
            self._angle += 2 * pi

    def to_float(self):
        self._adjust()
        return self._angle
    
    def to_positive_float(self):
        self._adjust()
        if(self._angle < 0):
            return self._angle + 2 * pi
        else:
            return self._angle
        
    def __add__(self, other: Self) -> Self:
        return Angle(self._angle + other._angle)
    
    def __iadd__(self, other: float) -> Self:
        return Angle(self._angle + other)
    
    def __sub__(self, other: Self) -> Self:
        return Angle(self._angle - other._angle)
    
    def __isub__(self, other: float) -> Self:
        return Angle(self._angle - other)
     
    def __eq__(self, other: Self) -> bool:
        return self._angle == other._angle 
    
    def __str__(self) -> str:
        return f"{self._angle} rad"
    
    @classmethod
    def compute_angle(cls, start_x: float, start_y: float, end_x: float, end_y: float) -> Self:
        if fabs(end_x - start_x) < 1 and fabs(end_y - start_y) < 1:
            # Not necessary
            return Angle(0)
        delta_x = end_x - start_x
        if delta_x == 0:
            if end_y < end_x:
                return Angle(3.0 * pi / 2.0)
            else:
                return Angle(pi / 2)
        elif delta_x > 0:
            return Angle(atan((end_y - start_y)/(end_x - start_x)))
        else:
            return Angle(pi + atan((end_y - start_y) / (end_x - start_x)))