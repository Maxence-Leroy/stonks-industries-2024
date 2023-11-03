import asyncio
from enum import Enum
from typing import Self
from collections.abc import Callable, Awaitable

from src.constants import MATCH_TIME
from src.location import Location
from src.logging import logging_info, logging_warning
from src.robot import robot
from src.robot_actuator import RobotBinaryActuator

class ActionFailedException(Exception):
    """Generic class for handling action failures"""

    pass

class PreconditionFailedException(ActionFailedException):
    """Class to raise an error when the `can_be_executed` function returned false"""

    pass

class ActionTimedOutException(ActionFailedException):
    """Class to raise an error when the `timer_limit` of an action has been reached"""

    pass

class ActionStatus(Enum):
    """Possible statuses of an action.
    
    Will be used to retry some precondition failed actions without retrying the done ones.

    Values
    ------
    WAITING: Action has been created but not tried yet

    PRE_CONDITION_FAILED: `can_be_executed` returned false when trying to execute the action

    TIMED_OUT: The action timed out, either before starting or while doing it

    FAILED: Action failed for another reason

    DOING: Action is in progress

    DONE: Action is done
    """

    WAITING = 0
    PRE_CONDITION_FAILED = 1
    TIMED_OUT = 2
    FAILED = 3
    DOING = 4
    DONE = 5
class Action:
    """An action is anything that can be done by the robot.
    
    Attributes
    ----------
    status: ActionStatus
        Current status of the action, `WAITING` by default

    timer_limit: float
        Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

    can_be_executed: Callable[[], bool]
        Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
        `True` by default

    affect_state: Callable[[], None]
        Function executed after the action to indicate the state change of the robot and the playing area, `None` by default

    Methods
    -------
    exec()
        Execute the action
    """

    async def _empty_function(self):
        return

    execute: Callable[[Self], Awaitable[None]] = _empty_function
    status: ActionStatus

    def __init__(
        self,
        timer_limit: float,
        can_be_executed: Callable[[], bool],
        affect_state: Callable[[], None],
    ):
        """
        Parameters
        ----------
        timer_limit: float
            Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

        can_be_executed: Callable[[], bool]
            Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
            `True` by default

        affect_state: Callable[[], None]
            Function executed after the action to indicate the state change of the robot and the playing area, `None` by default
        """

        self.timer_limit = timer_limit
        self.can_be_executed = can_be_executed
        self.affect_state = affect_state
        self.status = ActionStatus.WAITING

    def _has_no_condition(self) -> bool:
        """Helper function to write string representation of the action"""

        true_lambda = lambda: True
        return (true_lambda.__code__.co_consts == self.can_be_executed.__code__.co_consts and 
            true_lambda.__code__.co_code == self.can_be_executed.__code__.co_code)
    
    def __str__(self) -> str:
        return f"(timeout {self.timer_limit} conditions {"none" if self._has_no_condition() else "some"})"

    def _timeout(self) -> float:
        """Retrieve robot time and timer_limit. If result < 0, the action should be timed out."""

        current_time = robot.get_current_time()
        return self.timer_limit - current_time

    async def exec(self) -> None:
        """Execute the action. 
        
        This function takes care of handling `can_be_executed`, `timer_limit` and `affect_state`.
        
        Raises
        ------
        PreconditionFailedException
            If `can_be_executed` returns `False``

        ActionTimedOutException
            If the action timed out
        """

        action_short = self.__str__().split("\n")[0]
        if not self.can_be_executed():
            logging_warning(f"Unable to execute {action_short}")
            self.status = ActionStatus.PRE_CONDITION_FAILED
            raise PreconditionFailedException()

        timeout = self._timeout()

        if timeout < 0:
            logging_warning(f"Timeout before starting {action_short}")
            self.status = ActionStatus.TIMED_OUT
            raise ActionTimedOutException()

        try:
            logging_info(f"Start {action_short}")
            self.status = ActionStatus.DOING
            await asyncio.wait_for(self.execute(), timeout=timeout) # type: ignore
            self.status = ActionStatus.DONE
        except asyncio.TimeoutError:
            logging_warning(f"Unable to finish ${action_short}")
            self.handle_timeout_error_while_doing()
            self.status = ActionStatus.TIMED_OUT
            raise ActionTimedOutException()
        except Exception as ex:
            logging_warning(f"Action failed {action_short}")
            self.status = ActionStatus.FAILED
            raise ex

        logging_info(f"Apply state change {action_short}")
        self.affect_state()
        return
    
    def handle_timeout_error_while_doing(self) -> None:
        """Method to be overriden in children classes. This method is called if the action times out while doing it. 
        It is not called if the action times out before doing it."""

        pass


class ActionsSequence(Action):
    """Group of actions. They are done in the order given in parameter. 
    If one fails, the execution either goes to the next one or stops and the exception is transmited.
    """
    def __init__(
        self,
        actions: list[Action],
        allows_fail: bool,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        """
        Parameters
        ----------
        actions: list[Action]
            List of all actions in the right order

        allows_fail: bool
            If true, when one action fails, the next ones are executed. Otherwise, an exception is raised.

        timer_limit: float
            Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

        can_be_executed: Callable[[], bool]
            Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
            `True` by default

        affect_state: Callable[[], None]
            Function executed after the action to indicate the state change of the robot and the playing area, `None` by default
        """

        super().__init__(timer_limit, can_be_executed, affect_state)
        self.actions = actions
        self.allows_fail = allows_fail
    
    def __str__(self) -> str:
        string = f"Sequence of actions (allows fail {self.allows_fail}) {super().__str__()})\n"
        for action in self.actions:
            string += f"  {str(action)}\n"
        return string

    async def execute_multiple_actions(self) -> None:
        for action in self.actions:
            try: 
                await action.exec()
            except Exception as ex:
                if self.allows_fail:
                    pass
                else:
                    raise ex

        return

    execute: Callable[[Self], Awaitable[None]] = execute_multiple_actions

class Move(Action):
    """Action to move the position of the robot. The destination can either be an absolute location
    (using `Coordinates`) or the best possibility among many places (using `BestAvailable`)
    """

    def __init__(
        self,
        destination: Location,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        """
        Parameters
        ----------
        destination: Location
            The destination of the robot, it can either be an absolute location or the best possibility among many places.

        timer_limit: float
            Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

        can_be_executed: Callable[[], bool]
            Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
            `True` by default

        affect_state: Callable[[], None]
            Function executed after the action to indicate the state change of the robot and the playing area, `None` by default
        """
                
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.destination = destination

    def __str__(self) -> str:
        return f"Move to {str(self.destination)} {super().__str__()}"

    async def go_to_location(self) -> None:
        (x, y, theta) = self.destination.getLocation()
        await robot.go_to(x, y, theta)

    execute: Callable[[Self], Awaitable[None]] = go_to_location

    def handle_timeout_error_while_doing(self) -> None:
        robot.stop_moving() # If it times out the robot must stops


class Wait(Action):
    """Action to make the robt waits for a specific moment.
    I don't know if it will be needed or not, but I did it for the tests and because it's an easy one.
    """

    def __init__(
        self,
        time: float,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        """
        Parameters
        ----------
        time: float
            Time to wait in seconds

        timer_limit: float
            Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

        can_be_executed: Callable[[], bool]
            Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
            `True` by default

        affect_state: Callable[[], None]
            Function executed after the action to indicate the state change of the robot and the playing area, `None` by default
        """
                
        super().__init__(timer_limit, can_be_executed, affect_state)
        self.time = time

    def __str__(self) -> str:
        return f"Wait {self.time}s {super().__str__()}"

    async def wait(self) -> None:
        await asyncio.sleep(self.time)
        return

    execute: Callable[[Self], Awaitable[None]] = wait


class Switch(Action):
    """The robot has many actuators. This action allows to move a binary one (it can only be 0 or 1)."""

    def __init__(
        self,
        actuator: RobotBinaryActuator,
        on: bool,
        timer_limit: float = MATCH_TIME,
        can_be_executed: Callable[[], bool] = lambda: True,
        affect_state: Callable[[], None] = lambda: None,
    ):
        """
        Parameters
        ----------
        actuator: RobotBinaryActuator
            A reference to the robot actuator. Can be called directly with `robot.actuator`

        on: bool
            If true, the value 1 will be set. Otherwise it will be 0.
        
        timer_limit: float
            Time limit to do the action (time counted since the begining of the match), `MATCH_TIME` by default

        can_be_executed: Callable[[], bool]
            Function where we usually check the state of the robot and the playing area to know if the action is worth doing now,
            `True` by default

        affect_state: Callable[[], None]
            Function executed after the action to indicate the state change of the robot and the playing area, `None` by default
        """
        
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