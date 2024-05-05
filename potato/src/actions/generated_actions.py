from src.actions.action import Action, MoveServoContinous, Switch, ActionsInParallel
from src.constants import ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT
from src.robot import robot

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

def start_magnets() -> Action:
    return ActionsInParallel(actions=[
        Switch(
            robot.magnet1,
            on = True
        ),
        Switch(
            robot.magnet2,
            on = True
        ),
        Switch(
            robot.magnet3,
            on = True
        )
    ], allows_fail=True)

def stop_magnets() -> Action:
    return ActionsInParallel(actions=[
        Switch(
            robot.magnet1,
            on = False
        ),
        Switch(
            robot.magnet2,
            on = False
        ),
        Switch(
            robot.magnet3,
            on = False
        )
    ], allows_fail=True)