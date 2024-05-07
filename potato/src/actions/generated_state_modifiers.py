from src.robot.robot import robot
from src.playing_area import playing_area

def has_dropped_plants() -> None:
    if robot.state.plants_left > 0:
        robot.state.plants_left -= 1
        robot.state.plants_in_pots += 1

    if robot.state.plants_mid > 0:
        robot.state.plants_mid -= 1
        robot.state.plants_in_pots += 1

    if robot.state.plants_right > 0:
        robot.state.plants_right -= 1
        robot.state.plants_in_pots += 1
    
    robot.state.pots = 0

def has_captured_pots() -> None:
    robot.state.pots = 3
    robot_position = robot.current_location
    pot_coordinates = playing_area.get_closest_pot(robot_position.x, robot_position.y, robot_position.theta)
    if pot_coordinates is not None:
        best_pot = next((pot for pot in playing_area.pot_areas if pot.zone.x_center == pot_coordinates[0] and pot.zone.y_center == pot_coordinates[1]), None)
        if best_pot is not None:
            best_pot.has_pots = False

def drop_plants_in_planter() -> None:
    robot.state.pots = 0
    robot.state.score += 5 * robot.state.plants_in_pots
    robot.state.plants_in_pots = 0

    robot_position = robot.current_location
    planter_coordinates = playing_area.get_closest_pot(robot_position.x, robot_position.y, robot_position.theta)
    if planter_coordinates is not None:
        best_planter = next((planter for planter in playing_area.planters if planter.coordinates.x == planter_coordinates[0] and planter.coordinates.y == planter_coordinates[1]), None)
        if best_planter is not None:
            best_planter.has_pots = True

def has_captured_plants() -> None:
    robot_position = robot.current_location
    plant_zone = playing_area.get_closest_plant(robot_position.x, robot_position.y, robot_position.theta)
    if plant_zone is not None:
        index = playing_area.plant_areas.index(plant_zone)
        playing_area.plant_areas[index].has_plants = False

def has_arrived_in_end_area():
    robot.state.score += 10