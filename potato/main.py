import asyncio
import math
import time

from src.actions.action import ActionsSequence, Move
from src.actions.generated_actions import *
from src.constants import *
from src.location.location import MoveForward, SideRelatedCoordinates, RelativeMove
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot.robot import robot
from src.screen import screen

def main():
    screen.show_robot_name_and_side(None)
    playing_area.side = Side.BLUE
    open_replay_file()

    logging_info("Starting")

    robot.set_initial_position(SideRelatedCoordinates(100 + ROBOT_DEPTH / 2, 100 + ROBOT_DEPTH / 2, 0, playing_area.side))
    robot.wait_to_start()

    logging_info("Ready to start")
    time.sleep(5)

    strategy = ActionsSequence(
        timer_limit=MATCH_TIME,
        actions= [
            fetch_plants_and_put_them_in_planter(),
            fetch_plants_and_put_them_in_planter(),
            fetch_plants_and_put_them_in_planter(),
            go_to_end_area()
        ],
        allows_fail=False
    )

    logging_info(str(strategy))

    playing_area.set_used_start_area(robot.current_location.x, robot.current_location.y, robot.current_location.theta)
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
