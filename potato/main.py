import asyncio
import time

from src.actions.action import ActionsSequence
from src.actions.generated_actions import *
from src.constants import *
from src.logging import logging_info, start, logging_error
from src.playing_area import playing_area
from src.replay.save_replay import start_replay, open_replay_file
from src.robot.robot import robot
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
