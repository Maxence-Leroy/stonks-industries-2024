import asyncio
from typing import Optional, Self
from collections.abc import Callable, Awaitable

from src.location import Location
from src.logging import logging_info, logging_warning
from src.singletons import robot
from src.robot_actuator import RobotBinaryActuator

class Action:
    execute: Optional[Callable[[Self], Awaitable[bool]]] = None

    def __init__(
        self,
        timer_limit: Optional[float],
        can_be_executed: Callable[[], bool],
        affect_state: Callable[[], None],
    ):
        self.timer_limit = timer_limit
        self.can_be_executed = can_be_executed
        self.affect_state = affect_state

    def _has_no_condition(self) -> bool:
        true_lambda = lambda: True
        return (true_lambda.__code__.co_consts == self.can_be_executed.__code__.co_consts and 
            true_lambda.__code__.co_code == self.can_be_executed.__code__.co_code)
    
    def __str__(self) -> str:
        return f"(timeout {self.timer_limit} conditions {"none" if self._has_no_condition() else "some"})"

    def timeout(self) -> float | None:
        if self.timer_limit is None:
            return None
        current_time = robot.get_current_time()
        return self.timer_limit - current_time

    async def exec(self) -> bool:
        action_short = self.__str__().split("\n")[0]
        if not self.can_be_executed():
            logging_warning(f"Unable to execute {action_short}")
            return False

        timeout = self.timeout()

        if timeout is not None and timeout < 0:
            logging_warning(f"Timeout before starting {action_short}")
            return False

        result: None | bool = None
        if self.execute is None:
            result = True
        else:
            try:
                logging_info(f"Start {action_short}")
                result = await asyncio.wait_for(self.execute(), timeout=timeout)
            except asyncio.TimeoutError:
                logging_warning(f"Unable to finish ${action_short}")
                robot.stop()
                return False

        if not result:
            logging_warning(f"Action failed {action_short}")
            return False

        logging_info(f"Apply state change {action_short}")
        self.affect_state()
        return True


class ActionsSequence(Action):
    def __init__(
        self,
        actions: list[Action],
        timer_limit: float | None = None,
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

    async def execute_multiple_actions(self) -> bool:
        for action in self.actions:
            res = await action.exec()
            if not res:
                return False

        return True

    execute: Optional[Callable[[Self], Awaitable[bool]]] = execute_multiple_actions


class Move(Action):
    def __init__(
        self,
        destination: Location,
        timer_limit: float | None = None,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.destination = destination

    def __str__(self) -> str:
        return f"Move to {str(self.destination)} {super().__str__()}"

    async def go_to_location(self) -> bool:
        (x, y, theta) = self.destination.getLocation()
        return await robot.go_to(x, y, theta, self.timer_limit)

    execute: Optional[Callable[[Self], Awaitable[bool]]] = go_to_location


class Wait(Action):
    def __init__(
        self,
        time: float,
        timer_limit: float | None = None,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.time = time

    def __str__(self) -> str:
        return f"Wait {self.time}s {super().__str__()}"

    async def wait(self) -> bool:
        await asyncio.sleep(self.time)
        return True

    execute: Optional[Callable[[Self], Awaitable[bool]]] = wait


class Switch(Action):
    def __init__(
        self,
        actuator: RobotBinaryActuator,
        on: bool,
        timer_limit: float | None = None,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.actuator = actuator
        self.on = on

    def __str__(self) -> str:
        return f"Switch {self.actuator.name} {"on" if self.on else "off"} {super().__str__()}"

    async def switch(self):
        if self.on:
            self.actuator.switch_on()
        else:
            self.actuator.switch_off()

        return True

    execute: Optional[Callable[[Self], Awaitable[bool]]] = switch
