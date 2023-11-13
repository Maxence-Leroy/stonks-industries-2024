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

    def get_obstacles(self) -> list[tuple[int, int]]:
        obstacles: list[tuple[int, int]] = []
        for start_area in self.start_areas:
            if start_area.is_reserved:
                obstacles += start_area.zone.zone_with_robot_size().points_in_zone()
        for plant_area in self.plant_areas:
            if plant_area.has_plants:
                obstacles += plant_area.zone.zone_with_robot_size().points_in_zone()
        for pot_area in self.pot_areas:
            if pot_area.has_pots:
                obstacles += pot_area.zone.zone_with_robot_size().points_in_zone()

        return obstacles

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
