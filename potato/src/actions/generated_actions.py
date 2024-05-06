from src.actions.action import Action, MoveServoContinous, Switch, ActionsInParallel, CustomAction
from src.constants import ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT
from src.robot.robot import robot

def start_capturing_plants() -> Action:
    def action():
        robot.stepper_motors.write("L Start")
        robot.state.plant_canal_running = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT]

    return ActionsInParallel(
        actions=[
            MoveServoContinous(
                servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
                speed = 1000
            ),
            CustomAction(action_lambda=action)
        ],
        allows_fail=False
    )


def stop_capturing_plants() -> Action:
    def action():
        robot.stepper_motors.write("L Stop")
        robot.state.plant_canal_running = []

    return ActionsInParallel(
        actions=[
            MoveServoContinous(
                servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
                speed = 0
            ),
            CustomAction(action_lambda=action)
        ],
        allows_fail=False
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