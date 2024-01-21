import asyncio
import time

from src.action import ActionsSequence, Move
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import Coordinates, MoveForward
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
            Move(
                MoveForward(100)
            ),
            Move(
                Coordinates(1500, 1000, 0, side=playing_area.side)
            ),
            Move(
                Coordinates(ROBOT_DEPTH / 2 + 100, ROBOT_WIDTH / 2, 0),
                forced_angle=True
            ),
            Move(
                MoveForward(-100),
                backwards=True
            )
        ],
        allows_fail=False
    )
    robot.set_initial_position(Coordinates(ROBOT_DEPTH / 2, ROBOT_WIDTH / 2, 0, side=playing_area.side))
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
