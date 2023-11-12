from abc import ABC, abstractmethod
import time
from src.location import Coordinates

class Path(ABC):
    def __init__(self, going_backwards: bool) -> None:
        self._start_time = 0.0
        self._expected_duration = 0.0
        self._end_acceleration_time = 0.0
        self._start_decceleration_time = 0.0
        self._going_backwards = going_backwards

    @abstractmethod
    def expected_position(self, time: float) -> Coordinates:
        raise NotImplementedError()
    
    def start(self) -> None:
        self._start_time = time.time()

    def is_over(self) -> bool:
        ellapsed_time = time.time() - self._start_time
        return ellapsed_time > self._expected_duration or self._expected_duration == 0
    
    def is_going_backwards(self) -> bool:
        return self._going_backwards