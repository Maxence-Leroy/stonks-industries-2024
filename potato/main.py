import asyncio
import math
import time
from typing import List

from src.action import ActionsSequence, Move, MoveServoContinous, Wait
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import RelativeMove, SideRelatedCoordinates, MoveForward
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot

def main():
    playing_area.side = Side.BLUE
    robot.servo_ids = [7]
    open_replay_file()

    robot.wait_to_start()

    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions= [
            Move(SideRelatedCoordinates(500, 0, 0, playing_area.side)),
            Move(SideRelatedCoordinates(500, 500, 0, playing_area.side)),
            Move(SideRelatedCoordinates(0, 500, 0, playing_area.side)),
            Move(SideRelatedCoordinates(0, 0, 0, playing_area.side), forced_angle=True)
        ],
        allows_fail=False
    )

    logging_info(str(strategy))

    robot.start_time = time.time()
    start()
    start_replay()
    try:
        asyncio.run(strategy.exec())
    except Exception as ex:
        logging_error(f"Strategy failed: {ex}")
    logging_info("End of strategy")


if __name__ == "__main__":
    main()
