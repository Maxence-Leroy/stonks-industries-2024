# pyright: reportUnknownMemberType=false

import matplotlib
matplotlib.use('MacOSX')

import asyncio
from math import pi
import matplotlib.pylab as pl
import time

from src.action import ActionsSequence, Move, Wait
from src.constants import MATCH_TIME, Side
from src.location import Coordinates
from src.logging import logging_info, start
from src.playing_area import playing_area
from src.robot import robot


def main():
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            Move(
                destination=Coordinates(300, 0, pi / 2),
                forced_angle=True
            ),
            Wait(time=5.0),
            Move(
                destination= Coordinates(0,0,0),
                backwards=True
            )
        ],
        allows_fail=False
    )
    robot.set_initial_position(Coordinates(0, 0, 0))
    playing_area.side = Side.BLUE
    playing_area.compute_costs()

    print(playing_area.cost)
    pl.subplots(1, 1, figsize=(10,10))
    pl.grid(True)
    pl.xlim([0,60])
    pl.ylim([0,40])
    pl.margins(0)
    pl.imshow(playing_area.cost.transpose() > 1, aspect='auto', interpolation='nearest' )
    pl.show()

    logging_info(str(strategy))

    time.sleep(2.0)

    robot.start_time = time.time()
    start()
    asyncio.run(strategy.exec())
    logging_info(f"End of strategy")


if __name__ == "__main__":
    main()
