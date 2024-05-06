from enum import Enum
import math
from typing import Optional

from src.constants import *
from src.playing_area import playing_area
from src.location.location import Location

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
                closest_pot = playing_area.get_closest_pot(current_x, current_y, current_theta)
                if closest_pot is None:
                    return None
                vector = (closest_pot.zone.x_center - current_x, closest_pot.zone.y_center - current_y)
                norm = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                normalized_vector = (vector[0] / norm, vector[1] / norm)
                distance = norm - MARGIN__POT
                new_vector = (distance * normalized_vector[0], distance * normalized_vector[1])
                required_theta: float
                if closest_pot.zone.x_center == 35:
                    required_theta = 0
                elif closest_pot.zone.y_center == 35:
                    required_theta = math.pi/2
                elif closest_pot.zone.x_center == 2965:
                    required_theta = math.pi
                else:
                    required_theta = -math.pi/2

                return (new_vector[0], new_vector[1], required_theta) 
            
            case ImportantLocation.PLANT:
                closest_plant = playing_area.get_closest_plant(current_x, current_y, current_theta)
                if closest_plant is None:
                    return None
                vector = (closest_plant.zone.x_center - current_x, closest_plant.zone.y_center - current_y)
                norm = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                normalized_vector = (vector[0] / norm, vector[1] / norm)
                distance = norm - MARGIN_PLANT
                new_vector = (distance * normalized_vector[0], distance * normalized_vector[1])

                return (new_vector[0], new_vector[1], 0)
            
            case ImportantLocation.PLANTER:
                closest_planter = playing_area.get_best_planter(current_x, current_y, current_theta)
                if closest_planter is None:
                    return None
                vector = (closest_planter.coordinates.x - current_x, closest_planter.coordinates.y - current_y)
                norm = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                normalized_vector = (vector[0] / norm, vector[1] / norm)
                distance = norm - MARGIN_PLANTER - ROBOT_DEPTH / 2
                new_vector = (distance * normalized_vector[0], distance * normalized_vector[1])
                return (new_vector[0], new_vector[1], closest_planter.coordinates.theta) 
                
            case ImportantLocation.SOLAR_PANNEL_BEGIN:
                return playing_area.get_solar_pannel_begin()
            case ImportantLocation.SOLAR_PANNEL_END:
                return playing_area.get_solar_pannel_end()
            case ImportantLocation.END_AREA:
                closest_end_area = playing_area.get_best_start_area(current_x, current_y, current_theta)
                if closest_end_area is None:
                    return None
                center = closest_end_area.zone.center()
                return (center[0], center[1], 0)
