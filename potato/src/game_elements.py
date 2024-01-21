from dataclasses import dataclass
from typing import Optional

from src.constants import Side
from src.location.location import AbsoluteCoordinates
from src.zone import Circle, Rectangle

@dataclass
class StartArea():
    is_reserved: bool
    zone: Rectangle
    side: Side

@dataclass
class PlantArea():
    has_plants: bool
    zone: Circle

@dataclass
class PotArea():
    has_pots: bool
    zone: Circle

@dataclass
class Planter():
    has_pots: bool
    coordinates: AbsoluteCoordinates
    side: Side
    blocked_by:Optional[PotArea]

@dataclass
class OtherRobot():
    zone: Circle