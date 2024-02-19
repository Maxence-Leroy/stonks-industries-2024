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

    def string_name(self) -> str:
        match self:
            case EventType.ROBOT_POSITION:
                return "robot_position"
            case EventType.ROBOT_PATHING:
                return "robot_pathing"
            case EventType.ROBOT_DESTINATION:
                return "robot_destination"
            case _:
                return ""

@dataclass
class ReplayEvent:
    event: EventType
    place: Optional[tuple[float, float, float]] = None
    number: Optional[int] = None
    time: float = 0
