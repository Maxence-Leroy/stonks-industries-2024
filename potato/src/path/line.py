from math import sqrt, pow, acos, cos, sin, pi
from src.location import Coordinates
from src.path.angle import Angle
from src.path.path import Path

class Line(Path):
    def __init__(self, x_start: float, y_start: float, x_end: float, y_end: float, going_backwards: bool, max_speed: float = 500, max_acceleration: float = 500) -> None:
        super().__init__(going_backwards)
        self._x_start = x_start
        self._y_start = y_start
        self._x_end = x_end
        self._y_end = y_end
        self._max_speed = max_speed
        self._max_acceleration = max_acceleration

        self._vector_x = 0.0
        self._vector_y = 0.0
        self._theta = Angle(0)

        self._acceleration_distance = 0.0
        self._distance_with_constant_speed = 0.0

        distance = sqrt(
            pow(self._x_start - self._x_end, 2) +
            pow(self._y_start - self._y_end, 2)
        )

        acceleration_time = self._max_speed / self._max_acceleration
        acceleration_distance = 0.5 * pow(acceleration_time, 2) * self._max_acceleration

        if distance == 0:
            self._vector_x = 1
            self._vector_y = 0
            self._theta = Angle(0)
        else:
            self._vector_x = (self._x_end - self._x_start) / distance
            self._vector_y = (self._y_end - self._y_start) / distance
            self._theta = Angle(acos(self._vector_x))

            if self._vector_y < 0:
                self._theta += (2 * pi)

            if self.is_going_backwards():
                self._theta += pi


            if 2 * acceleration_distance > distance:
                # Short distance, we don't have time to reach full speed
                self._acceleration_distance = distance / 2
                self._distance_with_constant_speed = 0
                acceleration_time = sqrt(2 * self._acceleration_distance / self._max_acceleration)

                self._end_acceleration_time = acceleration_time
                self._start_decceleration_time = acceleration_time
                self._expected_duration = 2 * acceleration_time
            else:
                # Long distance, we will reach full speed
                self._acceleration_distance = acceleration_distance
                self._distance_with_constant_speed = distance - 2 * acceleration_distance

                self._end_acceleration_time = acceleration_time
                self._start_decceleration_time = acceleration_time + self._distance_with_constant_speed / self._max_speed
                self._expected_duration = self._start_decceleration_time + acceleration_time

    def expected_position(self, time: float) -> Coordinates:
        ellapsed_time = time - self._start_time
        
        if ellapsed_time < 0:
            return Coordinates(self._x_start, self._y_start, self._theta)
        elif 0 < ellapsed_time < self._end_acceleration_time:
            expected_x = self._x_start + self._vector_x * 0.5 * self._max_acceleration * pow(ellapsed_time, 2)
            expected_y = self._y_start + self._vector_y * 0.5 * self._max_acceleration * pow(ellapsed_time, 2)
            return Coordinates(expected_x, expected_y, self._theta)
        elif self._end_acceleration_time < ellapsed_time < self._start_decceleration_time:
            expected_x = self._x_start + self._vector_x * (self._acceleration_distance + (ellapsed_time - self._end_acceleration_time) * self._max_speed)
            expected_y = self._y_start + self._vector_y * (self._acceleration_distance + (ellapsed_time - self._end_acceleration_time) * self._max_speed)
            return Coordinates(expected_x, expected_y, self._theta)
        elif self._start_decceleration_time < ellapsed_time < self._expected_duration:
            expected_x = self._x_end - self._vector_x * 0.5 * self._max_acceleration * pow(self._expected_duration - ellapsed_time, 2)
            expected_y = self._y_end - self._vector_y * 0.5 * self._max_acceleration * pow(self._expected_duration - ellapsed_time, 2)
            return Coordinates(expected_x, expected_y, self._theta)
        else:
            return Coordinates(self._x_end, self._y_end, self._theta)
