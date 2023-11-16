import asyncio
import math
import time

from src.action import ActionsSequence, Move, Wait
from src.constants import MATCH_TIME, Side
from src.location.location import MoveForward, Coordinates, RelativeMove
from src.location.best_available import BestAvailable, ImportantLocation
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay
from src.robot import robot

def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                destination=BestAvailable(ImportantLocation.PLANT),
                pathfinding=True
            ),
            Move(
                destination = MoveForward(10)
            ),
            Move(
                destination=MoveForward(-10),
                backwards=True
            ),
            Wait(1.0),
            Move(
                destination=BestAvailable(ImportantLocation.POT),
                pathfinding=True
            ),
            Move(
                destination=MoveForward(-200),
                backwards=True
            ),
            Move(
                destination=RelativeMove(0, 0, math.pi),
            ),
            Move(
                destination=MoveForward(-210),
                backwards=True
            ),
            Wait(1.0),
            Move(
                destination=BestAvailable(ImportantLocation.PLANTER),
                pathfinding=True
            ),
            Move(
                destination=RelativeMove(0, 0, math.pi),
                forced_angle=True
            ),
            Move(
                destination=MoveForward(-10),
                backwards=True
            ),
            Wait(1.0),
            Move(
                destination=Coordinates(0, 0, 0),
                pathfinding=True
            )
        ],
        allows_fail=False
    )
    robot.set_initial_position(Coordinates(0, 0, 0))
    playing_area.side = Side.YELLOW
    playing_area.compute_costs()

    logging_info(str(strategy))

    time.sleep(2.0)

    robot.start_time = time.time()
    start()
    start_replay()
    try:
        asyncio.run(strategy.exec())
    except Exception as ex:
        logging_error(f"Strategy failed: {ex}")
    logging_info(f"End of strategy")


if __name__ == "__main__":
    main()
