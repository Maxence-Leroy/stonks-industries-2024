import asyncio
import time
import numpy as np

from src.actions.action import ActionsSequence, Move
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import SideRelatedCoordinates, MoveForward
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot

# ss = np.array([[1, 0], [1, 1], [0, 1], [0, 0]])
n = 8
z = np.exp(2j*np.pi*np.arange(n)/n) - 1

side_length = 200

def main():
    open_replay_file()
    playing_area.side = Side.BLUE
    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions=[Move(SideRelatedCoordinates(ROBOT_DEPTH/2 + side_length*z[(i+1)%n].imag, ROBOT_WIDTH/2 - side_length*z[(i+1)%n].real, 0, playing_area.side), forced_angle=(i==n-1)) for i in range(n)],
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
