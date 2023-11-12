from math import pow, fabs, sqrt

from src.location import Coordinates
from src.path.path import Path
from src.path.angle import Angle

class Rotation(Path):
    def __init__(self, x: float, y:float, start_theta: Angle, end_theta: Angle, max_speed: float = 2, max_acceleration: float = 2) -> None:
        super().__init__(going_backwards=False)
        self._x = x
        self._y = y
        self._start_theta = start_theta
        self._end_theta = end_theta
        self._max_speed = max_speed
        self._max_acceleration = max_acceleration

        self._angle_for_acceleration = 0.0
        self._angle_with_constant_speed = 0.0

        self._direction = -1 if (self._end_theta - self._start_theta).to_float() < 0 else 1

        acceleration_duration = self._max_speed / self._max_acceleration
        acceleration_angle = 0.5 * self._max_acceleration * pow(acceleration_duration, 2)
        total_angle = fabs((self._end_theta - self._start_theta).to_float())

        if 2 * acceleration_angle >total_angle:
            # Small rotation, we don't have time to reach max speed
            acceleration_angle = total_angle / 2
            acceleration_duration = sqrt(2 * acceleration_angle / self._max_acceleration)

            self._angle_for_acceleration = acceleration_angle
            self._angle_with_constant_speed = 0
            self._end_acceleration_time = acceleration_duration
            self._start_decceleration_time = acceleration_duration
            self._expected_duration = 2 * acceleration_duration
        else:
            # Big rotation. We will reach max speed
            self._angle_for_acceleration = acceleration_angle
            self._angle_with_constant_speed = total_angle - 2 * acceleration_angle
            self._end_acceleration_time = acceleration_duration
            self._start_decceleration_time = self._end_acceleration_time + self._angle_with_constant_speed / self._max_speed
            self._expected_duration = self._start_decceleration_time + acceleration_duration

    def expected_position(self, time: float) -> Coordinates:
        ellapsed_time = time - self._start_time

        if ellapsed_time < 0:
            return Coordinates(self._x, self._y, self._start_theta)
        elif 0 < ellapsed_time < self._end_acceleration_time:
            expected_theta = self._start_theta + Angle(0.5* self._direction * self._max_acceleration * pow(ellapsed_time, 2))
            return Coordinates(self._x, self._y, expected_theta)
        elif self._end_acceleration_time < ellapsed_time < self._start_decceleration_time:
            expected_theta = self._start_theta + Angle(self._direction *(self._angle_for_acceleration + (ellapsed_time-self._end_acceleration_time) * self._max_speed))
            return Coordinates(self._x, self._y, expected_theta)
        elif self._start_decceleration_time < ellapsed_time < self._expected_duration:
            expected_theta = self._end_theta - Angle(0.5*self._direction*self._max_acceleration*pow((self._expected_duration-ellapsed_time), 2))
            return Coordinates(self._x, self._y, expected_theta)
        else:
            return Coordinates(self._x, self._y, self._end_theta)
