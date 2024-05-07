from src.actions.action import Move, Action, MoveServoContinous, Switch, ActionsInParallel, ActionsSequence, CustomAction, Wait
from src.location.best_available import BestAvailable, ImportantLocation
from src.location.location import MoveForward
from src.constants import *
from src.robot.robot import robot
from src.actions.generated_conditions import *
from src.actions.generated_state_modifiers import *

def fetch_plants_and_put_them_in_planter() -> Action:
    return ActionsSequence(
        actions= [
            ActionsSequence(
                actions= [
                    Move(BestAvailable(ImportantLocation.PLANT)),
                    start_capturing_plants(),
                    Move(MoveForward(2 * MARGIN_PLANT), max_speed=50),
                    Wait(3),
                    stop_capturing_plants(),
                ],
                allows_fail = False,
                affect_state= has_captured_plants
            ),
            ActionsSequence(
                actions= [
                    Move(BestAvailable(ImportantLocation.POT), forced_angle=True, precision=True),
                    start_magnets(),
                    Move(
                        MoveForward(MARGIN__POT),
                        backwards=True,
                        max_speed=33,
                        max_acceleration=33,
                        precision= True
                    ),
                ],
                can_be_executed = has_plants,
                affect_state=has_captured_pots,
                allows_fail=False,
            ),
            ActionsSequence(
                actions= [
                    ActionsInParallel(
                        actions=[
                            Move(
                                BestAvailable(ImportantLocation.PLANTER),
                                forced_angle=True,
                                precision=True
                            ),
                            drop_plants_in_pot()
                        ],
                        allows_fail=True
                    ),
                    Move(
                        MoveForward(MARGIN_PLANTER),
                        backwards=True,
                        max_speed=33,
                        max_acceleration=33,
                        precision= True
                    ),
                    stop_magnets()
                ],
                allows_fail=False,
                can_be_executed= has_plants_and_pots,
                affect_state=drop_plants_in_planter
            ),
        ],            
        allows_fail=True
    )

def start_capturing_plants() -> Action:
    def action():
        robot.stepper_motors.write("L Start\n")
        robot.state.plant_canal_running = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT]

    return ActionsInParallel(
        actions= [
            Switch(
                actuator = robot.left_laser,
                on = True
            ),
            Switch(
                actuator = robot.mid_laser,
                on = True
            ),
            Switch(
                actuator = robot.right_laser,
                on = True
            ),
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
        robot.stepper_motors.write("L Stop\n")
        robot.state.plant_canal_running = []

    return ActionsInParallel(
        actions=[
            Switch(
                actuator = robot.left_laser,
                on = False
            ),
            Switch(
                actuator = robot.mid_laser,
                on = False
            ),
            Switch(
                actuator = robot.right_laser,
                on = False
            ),
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

def drop_plants_in_pot() -> Action:
    return ActionsSequence(
        actions=[
            MoveServoContinous(
                servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
                speed = 1000
            ),
            Wait(5),
            MoveServoContinous(
                servo_ids = [ID_SERVO_PLANT_LEFT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_RIGHT],
                speed = 0   
            )
        ],
        allows_fail=False,
        affect_state=has_dropped_plants
    )

def go_to_end_area() -> Action:
    return Move(
        BestAvailable(ImportantLocation.END_AREA),
        affect_state=has_arrived_in_end_area
    )