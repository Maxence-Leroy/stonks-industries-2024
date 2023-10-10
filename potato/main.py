import asyncio
import time

from src.action import ActionsSequence, Move, Switch, Wait
from src.constants import MATCH_TIME
from src.location import Coordinates
from src.singletons import robot


def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                timer_limit=80,
                destination=Coordinates(1, 1, 0),
            ),
            Switch(actuator=robot.led_ethernet, on=True),
            Wait(time=2.0),
            Switch(actuator=robot.led_ethernet, on=False),
        ],
    )

    print(strategy)

    time.sleep(2.0)

    robot.start_time = time.time()
    success = asyncio.run(strategy.exec())
    print(f"Success {success}")


if __name__ == "__main__":
    main()
