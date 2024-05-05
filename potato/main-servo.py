import asyncio
import time

from src.actions.action import ActionsSequence, MoveServoTarget, MoveServoContinous, Wait
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import SideRelatedCoordinates
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot

def main():
    open_replay_file()
    ids = [1, 3]
    playing_area.side = Side.BLUE
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[
            #MoveServoTarget(ids, [0, 0], False),
            #Wait(1),
            #MoveServoTarget(ids, [4000, 4000], False),
            #Wait(2),
            MoveServoContinous(ids, -1000),
            Wait(5),
            MoveServoContinous(ids, 0)
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
