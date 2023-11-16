from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventType(int, Enum):
    ROBOT_POSITION = 0
    ROBOT_PATHING = 1
    ROBOT_DESTINATION = 2
    POT_GONE = 3
    PLANT_GONE = 4
    PLANT_IN_PLANTER = 5
    OBSTACLE_FOUND = 6
    OBSTACLE_DISAPPEAR = 7
    SCORE = 8

@dataclass
class ReplayEvent:
    event: EventType
    place: Optional[tuple[float, float, float]] = None
    number: Optional[int] = None
    time: float = 0
