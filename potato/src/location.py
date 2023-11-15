from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from src.playing_area import playing_area


class Location(ABC):
    """Abstract class for a location. Has a method `getLocation` that will be called when the move location is starting"""

    @abstractmethod
    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        raise NotImplementedError()


class Coordinates(Location):
    """Location with "absolute" coordinates. They will be converted according to the side of the playing area."""

    def __init__(self, x: float, y: float, theta: float) -> None:
        """
        Parameters
        ----------
        x: float
            X position in mm

        y: float
            Y position in mm

        theta: float
            Angle of the robot in radians
        """

        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y}, θ: {self.theta})"

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        return (self.x, self.y, self.theta)


class ImportantLocation(Enum):
    """
    Enum of areas with a name. For some of them, they are multiple places on the playing area.
    The best available will be chosen depending on the state of the playing area

    POT: metal plot for the plant
    PLANT: plants
    PLANTER: place to put the plants once they are in pots
    SOLAR_PANNEL_BEGIN: one extremity of solar pannels (excluding opponents' reserved ones)
    SOLAR_PANNEL_END : other extremity of solar pannels (excluding opponents' reserved ones)
    END_AREA: one of the area the robot can finish the match
    """

    POT = 0
    PLANT = 1
    PLANTER = 2
    SOLAR_PANNEL_BEGIN = 3
    SOLAR_PANNEL_END = 4
    END_AREA = 5

class BestAvailable(Location):
    """Location from a place on the playing area. There can be multiple places for the same enum value.
    It will be converted in coordinates at the begining of the action (and using the right side of the playing area)
    """

    def __init__(self, location: ImportantLocation) -> None:
        """
        Parameters
        ----------
        location: ImportantLocation
            One of the pre-recorded locations
        """
                
        super().__init__()
        self.location = location

    def __str__(self) -> str:
        return f'Next {str(self.location).replace("_", " ").lower()}'

    def getLocation(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        match self.location:
            case ImportantLocation.POT:
                return playing_area.get_closest_pot(current_x, current_y, current_theta)
            case ImportantLocation.PLANT:
                return playing_area.get_next_plant()
            case ImportantLocation.PLANTER:
                return playing_area.get_next_planter()
            case ImportantLocation.SOLAR_PANNEL_BEGIN:
                return playing_area.get_solar_pannel_begin()
            case ImportantLocation.SOLAR_PANNEL_END:
                return playing_area.get_solar_pannel_end()
            case ImportantLocation.END_AREA:
                return playing_area.get_end_area()
