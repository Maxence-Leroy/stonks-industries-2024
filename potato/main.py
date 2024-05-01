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
    servo_id = 7
    robot.servo_ids = [servo_id]
    open_replay_file()
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions= [
            Move(MoveForward(-150)),
            Move(MoveForward(-150)),
        ],
        allows_fail=False
    )
    robot.set_initial_position(SideRelatedCoordinates(0, 0, 0, playing_area.side))
    #robot.set_initial_position(SideRelatedCoordinates(ROBOT_DEPTH / 2 + 100, ROBOT_WIDTH / 2 + 100, 0, playing_area.side))
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
    logging_info("End of strategy")


if __name__ == "__main__":
    main()
