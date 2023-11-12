import asyncio
import time

from src.action import ActionsSequence, Move, Wait
from src.constants import MATCH_TIME
from src.location import Coordinates
from src.logging import logging_info, start
from src.robot import robot


def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                destination=Coordinates(100, 0, 0)
            ),
            Wait(time=5.0),
            Move(
                destination= Coordinates(0,0,0),
                backwards=True
            )
        ],
        allows_fail=False
    )

    logging_info(str(strategy))

    time.sleep(2.0)

    robot.set_initial_position(Coordinates(0, 0, 0))
    robot.start_time = time.time()
    start()
    asyncio.run(strategy.exec())
    logging_info(f"End of strategy")


if __name__ == "__main__":
    main()
