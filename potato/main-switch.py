import asyncio
import time
import numpy as np

from src.action import ActionsSequence, Move
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH
from src.location.location import SideRelatedCoordinates, MoveForward
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot


def main():
    open_replay_file()
    playing_area.side = Side.BLUE
    robot.set_initial_position(SideRelatedCoordinates(ROBOT_DEPTH / 2, ROBOT_WIDTH / 2, 0, playing_area.side))
    playing_area.compute_costs()
    i = 0

    while True:
        i += 1
        print(i)
        print(f"Start { robot.start_switch.get_value()}")
        print(f"Side {robot.side_switch.get_value()}")
        print("")
        time.sleep(2)


if __name__ == "__main__":
    main()
