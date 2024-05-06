from src.robot.robot import robot

def has_plants() -> bool:
    return robot.state.plants_left > 0 or robot.state.plants_mid > 0 or robot.state.plants_right > 0

def has_plants_and_pots() -> bool:
    return has_plants() and robot.state.pots == 3

def has_plants_in_pots() -> bool:
    return robot.state.plants_in_pots > 0