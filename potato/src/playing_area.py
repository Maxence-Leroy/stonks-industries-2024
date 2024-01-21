from typing import Optional
import numpy as np
import math
from nptyping import NDArray, Float, Shape

from src.constants import ROBOT_DEPTH, Side, PLAYING_AREA_WIDTH, PLAYING_AREA_DEPTH, D_STAR_FACTOR
from src.game_elements import PlantArea, Planter, PotArea, StartArea, OtherRobot
from src.location.location import AbsoluteCoordinates
from src.logging import logging_warning
from src.zone import Circle, Rectangle, Zone

BIG_NUMBER = 10**10

class PlayingArea:
    """Class represenging the playing area.
    
    TODO: Add state
    """
    start_areas: list[StartArea]
    plant_areas: list[PlantArea]
    pot_areas: list[PotArea]
    planters: list[Planter]
    other_robot: OtherRobot
    obstacles_change: list[Zone]
    cost: NDArray[Shape["60,40"], Float]
    side: Side


    def __init__(self) -> None:
        self.cost = np.full((int(PLAYING_AREA_WIDTH / D_STAR_FACTOR), int(PLAYING_AREA_DEPTH /D_STAR_FACTOR)), 1.0)
        self.obstacles_change = []
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

        self.planters = [
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(0, 612.5, math.pi), side=Side.YELLOW, blocked_by=self.pot_areas[1]),
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(0, 1387.5, math.pi), side=Side.BLUE, blocked_by=self.pot_areas[2]),
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(762.5, 2000, math.pi/2), side=Side.BLUE, blocked_by=None),
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(2237.5, 2000, math.pi/2), side=Side.YELLOW, blocked_by=None),
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(3000, 1387.5, 0), side=Side.YELLOW, blocked_by=self.pot_areas[5]),
            Planter(has_pots=False, coordinates=AbsoluteCoordinates(3000, 612.5, 0), side=Side.BLUE, blocked_by=self.pot_areas[4]),
        ]
        self.other_robot = OtherRobot(Circle(PLAYING_AREA_WIDTH * 2, PLAYING_AREA_DEPTH * 2, 1200 / 8))

    def compute_costs(self):
        self.cost = np.full((int(PLAYING_AREA_WIDTH / D_STAR_FACTOR), int(PLAYING_AREA_DEPTH /D_STAR_FACTOR)), 1.0)
        for start_area in self.start_areas:
            if start_area.is_reserved and start_area.side != self.side:
                self.cost[start_area.zone.zone_with_robot_size().points_in_zone()] = BIG_NUMBER
        for plant_area in self.plant_areas:
            if plant_area.has_plants:
                self.cost[plant_area.zone.zone_with_robot_size().points_in_zone()] = BIG_NUMBER
        for pot_area in self.pot_areas:
            if pot_area.has_pots:
                self.cost[pot_area.zone.zone_with_robot_size().points_in_zone()] = BIG_NUMBER
        self.cost[self.other_robot.zone.zone_with_robot_size().points_in_zone()] = BIG_NUMBER

    def set_other_robot_position(self, x: float, y: float):
        if x != self.other_robot.zone.x_center or y != self.other_robot.zone.y_center:
            self.obstacles_change.append(self.other_robot.zone.zone_with_robot_size())
            self.other_robot.zone.x_center = x
            self.other_robot.zone.y_center = y
            self.obstacles_change.append(self.other_robot.zone.zone_with_robot_size())
            self.compute_costs()

    def get_closest_pot(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        min_distance = np.inf
        min_arg: Optional[PotArea] = None
        for pot_area in self.pot_areas:
            if pot_area.has_pots:
                distance = math.sqrt(math.pow(pot_area.zone.x_center - current_x, 2) + math.pow(pot_area.zone.y_center - current_y, 2))
                if distance < min_distance:
                    min_distance = distance
                    min_arg = pot_area
        if min_arg is None:
            logging_warning("No pot found")
            return None
        vector = (min_arg.zone.x_center - current_x, min_arg.zone.y_center - current_y)
        theta = math.atan2(vector[1], vector[0])
        return (min_arg.zone.x_center, min_arg.zone.y_center, theta)

    def get_closest_plant(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        min_distance = np.inf
        min_arg: Optional[PlantArea] = None
        for plant_area in self.plant_areas:
            if plant_area.has_plants:
                distance = math.sqrt(math.pow(plant_area.zone.x_center - current_x, 2) + math.pow(plant_area.zone.y_center - current_y, 2))
                if distance < min_distance:
                    min_distance = distance
                    min_arg = plant_area
        if min_arg is None:
            logging_warning("No plant found")
            return None
        vector = (min_arg.zone.x_center - current_x, min_arg.zone.y_center - current_y)
        theta = math.atan2(vector[1], vector[0])
        return (min_arg.zone.x_center, min_arg.zone.y_center, theta)

    def get_best_planter(self, current_x: float, current_y: float, current_theta: float) -> Optional[tuple[float, float, float]]:
        min_distance = np.inf
        min_arg: Optional[Planter] = None
        for planter in self.planters:
            if not planter.has_pots and (planter.blocked_by is None or not planter.blocked_by.has_pots):
                distance = math.sqrt(math.pow(planter.coordinates.x - current_x, 2) + math.pow(planter.coordinates.y - current_y, 2))
                if distance < min_distance:
                    min_distance = distance
                    min_arg = planter
        if min_arg is None:
            logging_warning("No planter found")
            return None
        x = min_arg.coordinates.x
        y = min_arg.coordinates.y
        theta = min_arg.coordinates.theta
        x -= math.cos(theta) * ROBOT_DEPTH / 2
        y -= math.sin(theta) * ROBOT_DEPTH / 2

        return (x, y, theta)

    def get_solar_pannel_begin(self) -> tuple[float, float, float]:
        return (4, 4, 4)

    def get_solar_pannel_end(self) -> tuple[float, float, float]:
        return (10, 10, 10)

    def get_end_area(self) -> tuple[float, float, float]:
        return (100, 100, 100)
    

playing_area = PlayingArea() # Singleton
