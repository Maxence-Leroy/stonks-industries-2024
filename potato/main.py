import asyncio
from math import pi
import time

from src.action import ActionsSequence, Move, Wait
from src.constants import MATCH_TIME, Side
from src.location import Coordinates
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.robot import robot


def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                destination=Coordinates(2990, 1990, pi / 2),
                forced_angle=True
            ),
            Wait(time=5.0),
            Move(
                destination= Coordinates(0,0,0),
                backwards=True,
                pathfinding=False
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
    try:
        asyncio.run(strategy.exec())
    except Exception as ex:
        logging_error(f"Strategy failed: {ex}")
    logging_info(f"End of strategy")


if __name__ == "__main__":
    main()
