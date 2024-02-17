import asyncio
import time

from src.action import ActionsSequence, MoveServoTarget, MoveServoContinous, Wait
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import SideRelatedCoordinates
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot

def main():
    open_replay_file()
    playing_area.side = Side.BLUE
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            MoveServoTarget([2], [0]),
            Wait(5),
            MoveServoTarget([2], [4000]),
            Wait(5),
            MoveServoContinous([2], -1000),
            Wait(5),
            MoveServoContinous([2], 0)
        ],
        allows_fail=False
    )
    robot.set_initial_position(SideRelatedCoordinates(ROBOT_DEPTH / 2, ROBOT_WIDTH / 2, 0, playing_area.side))
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
