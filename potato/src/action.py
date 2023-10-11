import asyncio
from enum import Enum
from typing import Self
from collections.abc import Callable, Awaitable

from src.constants import MATCH_TIME
from src.location import Location
from src.logging import logging_info, logging_warning
from src.singletons import robot
from src.robot_actuator import RobotBinaryActuator

class ActionFailedException(Exception):
    pass

class PreconditionFailedException(ActionFailedException):
    pass

class ActionTimedOutException(ActionFailedException):
    pass

ActionStatus = Enum(
    "ActionStatus",
    ["WAITING", "PRE_CONDITION_FAILED", "TIMED_OUT", "DOING", "DONE", "FAILED"],
)

class Action:
    async def empty_function(self):
        return

    execute: Callable[[Self], Awaitable[None]] = empty_function
    status: ActionStatus

    def __init__(
        self,
        timer_limit: float,
        can_be_executed: Callable[[], bool],
        affect_state: Callable[[], None],
    ):
        self.timer_limit = timer_limit
        self.can_be_executed = can_be_executed
        self.affect_state = affect_state
        self.status = ActionStatus.WAITING

    def _has_no_condition(self) -> bool:
        true_lambda = lambda: True
        return (true_lambda.__code__.co_consts == self.can_be_executed.__code__.co_consts and 
            true_lambda.__code__.co_code == self.can_be_executed.__code__.co_code)
    
    def __str__(self) -> str:
        return f"(timeout {self.timer_limit} conditions {"none" if self._has_no_condition() else "some"})"

    def timeout(self) -> float:
        current_time = robot.get_current_time()
        return self.timer_limit - current_time

    async def exec(self) -> None:
        action_short = self.__str__().split("\n")[0]
        if not self.can_be_executed():
            logging_warning(f"Unable to execute {action_short}")
            self.status = ActionStatus.PRE_CONDITION_FAILED
            raise PreconditionFailedException()

        timeout = self.timeout()

        if timeout < 0:
            logging_warning(f"Timeout before starting {action_short}")
            self.status = ActionStatus.TIMED_OUT
            raise ActionTimedOutException()

        try:
            logging_info(f"Start {action_short}")
            self.status = ActionStatus.DOING
            await asyncio.wait_for(self.execute(), timeout=timeout)
            self.status = ActionStatus.DONE
        except asyncio.TimeoutError:
            logging_warning(f"Unable to finish ${action_short}")
            self.handle_timeout_error()
            self.status = ActionStatus.TIMED_OUT
            raise ActionTimedOutException()
        except Exception as ex:
            logging_warning(f"Action failed {action_short}")
            self.status = ActionStatus.FAILED
            raise ex

        logging_info(f"Apply state change {action_short}")
        self.affect_state()
        return
    
    def handle_timeout_error(self) -> None:
        pass


class ActionsSequence(Action):
    def __init__(
        self,
        actions: list[Action],
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.actions = actions
    
    def __str__(self) -> str:
        string = f"Sequence of actions {super().__str__()})\n"
        for action in self.actions:
            string += f"  {str(action)}\n"
        return string

    async def execute_multiple_actions(self) -> None:
        for action in self.actions:
            try: 
                await action.exec()
            except Exception:
                pass

        return

    execute: Callable[[Self], Awaitable[None]] = execute_multiple_actions

class Move(Action):
    def __init__(
        self,
        destination: Location,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.destination = destination

    def __str__(self) -> str:
        return f"Move to {str(self.destination)} {super().__str__()}"

    async def go_to_location(self) -> None:
        (x, y, theta) = self.destination.getLocation()
        await robot.go_to(x, y, theta, self.timer_limit)

    execute: Callable[[Self], Awaitable[None]] = go_to_location

    def handle_timeout_error(self) -> None:
        robot.stop_moving()


class Wait(Action):
    def __init__(
        self,
        time: float,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.time = time

    def __str__(self) -> str:
        return f"Wait {self.time}s {super().__str__()}"

    async def wait(self) -> None:
        await asyncio.sleep(self.time)
        return

    execute: Callable[[Self], Awaitable[None]] = wait


class Switch(Action):
    def __init__(
        self,
        actuator: RobotBinaryActuator,
        on: bool,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.actuator = actuator
        self.on = on

    def __str__(self) -> str:
        return f"Switch {self.actuator.name} {"on" if self.on else "off"} {super().__str__()}"

    async def switch(self) -> None:
        if self.on:
            self.actuator.switch_on()
        else:
            self.actuator.switch_off()

        return

    execute: Callable[[Self], Awaitable[None]] = switch
