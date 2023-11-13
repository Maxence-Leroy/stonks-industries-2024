from src.constants import Side
from src.zone import Circle, Rectangle

class StartArea():
    is_reserved: bool
    zone: Rectangle
    side: Side

    def __init__(self, is_reserved: bool, zone: Rectangle, side: Side):
        self.is_reserved = is_reserved
        self.zone = zone
        self.side = side

class PlantArea():
    has_plants: bool
    zone: Circle

    def __init__(self, has_plants: bool, zone: Circle):
        self.has_plants = has_plants
        self.zone = zone

class PotArea():
    has_pots: bool
    zone: Circle

    def __init__(self, has_pots: bool, zone: Circle):
        self.has_pots = has_pots
        self.zone = zone