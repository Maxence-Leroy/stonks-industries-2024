from src.actions.action import Action, MoveServoContinous
from src.constants import ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT

def start_capturing_plants() -> Action:
    return MoveServoContinous(
        servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
        speed = 1000
    )

def stop_capturing_plants() -> Action:
    return MoveServoContinous(
        servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
        speed = 0
    )