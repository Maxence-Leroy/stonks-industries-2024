from src.constants import Side
from src.game_elements import PlantArea, PotArea, StartArea
from src.zone import Circle, Rectangle

class PlayingArea:
    """Class represenging the playing area.
    
    TODO: Add state
    """
    start_areas: list[StartArea]
    plant_areas: list[PlantArea]
    pot_areas: list[PotArea]

    def __init__(self) -> None:
        self.start_areas = [
            StartArea(is_reserved=False, zone=Rectangle(0, 0, 450, 450), side=Side.BLUE),
            StartArea(is_reserved=False, zone=Rectangle(0, 775, 450, 1225), side=Side.YELLOW),
            StartArea(is_reserved=True, zone=Rectangle(0, 1550, 450, 2000), side=Side.BLUE),
            StartArea(is_reserved=False, zone=Rectangle(2550, 0, 3000, 450), side=Side.YELLOW),
            StartArea(is_reserved=False, zone=Rectangle(2550, 775, 3000, 1225), side=Side.BLUE),
            StartArea(is_reserved=True, zone=Rectangle(2550, 1550, 3000, 2000), side=Side.YELLOW),
        ]

        self.plant_areas = [
            PlantArea(has_plants=True, zone=Circle(1000, 700, 125)),
            PlantArea(has_plants=True, zone=Circle(1000, 1300, 125)),
            PlantArea(has_plants=True, zone=Circle(1500, 1500, 125)),
            PlantArea(has_plants=True, zone=Circle(2000, 1300, 125)),
            PlantArea(has_plants=True, zone=Circle(2000, 700, 125)),
            PlantArea(has_plants=True, zone=Circle(1500, 500, 125))
        ]

        self.pot_areas = [
            PotArea(has_pots=True, zone=Circle(1000, 35, 125)),
            PotArea(has_pots=True, zone=Circle(35, 612.5, 125)),
            PotArea(has_pots=True, zone=Circle(35, 1387.5, 125)),
            PotArea(has_pots=True, zone=Circle(2000, 35, 125)),
            PotArea(has_pots=True, zone=Circle(2965, 612.5, 125)),
            PotArea(has_pots=True, zone=Circle(2965, 1387.5, 125))
        ]

    def get_next_pot(self) -> tuple[float, float, float]:
        return (0, 0, 0)

    def get_next_plant(self) -> tuple[float, float, float]:
        return (1, 1, 1)

    def get_next_planter(self) -> tuple[float, float, float]:
        return (2, 2, 2)

    def get_solar_pannel_begin(self) -> tuple[float, float, float]:
        return (4, 4, 4)

    def get_solar_pannel_end(self) -> tuple[float, float, float]:
        return (10, 10, 10)

    def get_end_area(self) -> tuple[float, float, float]:
        return (100, 100, 100)
    

playing_area = PlayingArea() # Singleton
