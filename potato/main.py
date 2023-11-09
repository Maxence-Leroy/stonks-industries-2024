import asyncio
import time

from src.action import ActionsInParallel, ActionsSequence, Move, Switch, Wait
from src.constants import MATCH_TIME
from src.location import Coordinates
from src.logging import logging_info
from src.robot import robot


def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                timer_limit=80,
                destination=Coordinates(10, 10, 0),
            ),
            Wait(time=5.0),
            Move(
                timer_limit = 5,
                destination= Coordinates(0,0,0)
            )
        ],
        allows_fail=False
    )

    logging_info(str(strategy))

    time.sleep(2.0)

    robot.start_time = time.time()
    asyncio.run(strategy.exec())
    logging_info(f"End of strategy")


if __name__ == "__main__":
    main()
