import asyncio
import math
import time
from typing import List

from src.actions.action import ActionsSequence, Move, Wait
from src.actions.generated_actions import *
from src.constants import MATCH_TIME, Side, ROBOT_WIDTH, ROBOT_DEPTH, ID_SERVO_PLANT_RIGHT, ID_SERVO_PLANT_MID, ID_SERVO_PLANT_LEFT
from src.location.location import SideRelatedCoordinates, MoveForward
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot import robot
from src.screen import screen

def main():
    logging_info("Starting")
    screen.show_robot_name_and_side(None)
    playing_area.side = Side.BLUE
    open_replay_file()

    robot.wait_to_start()

    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions= [
            start_magnets(),
            Move(SideRelatedCoordinates(100, 0, 0, playing_area.side)),
            start_capturing_plants(),
            Move(SideRelatedCoordinates(300, 0, 0, playing_area.side), max_speed = 20, max_acceleration = 20),
            Wait(20),
            stop_capturing_plants(),
            stop_magnets()
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
