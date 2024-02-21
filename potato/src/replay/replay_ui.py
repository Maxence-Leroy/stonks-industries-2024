from dataclasses import dataclass, field
import math
import os
import time as time_library
from typing import Optional
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

from src.constants import PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH, MATCH_TIME
from src.helpers.pairwise import pairwise
from src.replay.base_classes import ReplayEvent, EventType

MM_TO_PIXEL_DIVIDER = 4
SLIDER_WIDTH = 100
MARGIN = 10
WINDOW_SIZE = [PLAYING_AREA_WIDTH / MM_TO_PIXEL_DIVIDER + 2 * MARGIN + SLIDER_WIDTH, PLAYING_AREA_DEPTH / MM_TO_PIXEL_DIVIDER]


@dataclass
class ReplayState:
    robot_path: list[tuple[float, float, float]] = field(default_factory=list)
    robot_position: Optional[tuple[float, float, float]] = None
    robot_goal: Optional[tuple[float, float, float]] = None
    obstacles: list[tuple[float, float, float]] = field(default_factory=list)

def compute_state(events: list[ReplayEvent], time: float) -> ReplayState:
    events.sort(key=lambda event: event.time)
    state = ReplayState()
    for event in events:
        if event.time > time:
            break
        if event.event == EventType.ROBOT_POSITION:
            state.robot_position = event.place
        elif event.event == EventType.ROBOT_DESTINATION:
            state.robot_path = []
            state.robot_goal = event.place
        elif event.event == EventType.ROBOT_PATHING:
            if event.place is None:
                raise ValueError()
            state.robot_path.append(event.place)

    state.obstacles = []
    obstacle_events = list(filter(lambda event: event.event == EventType.LIDAR and event.time <= time, events))
    if len(obstacle_events) > 0:
        max_time_obstacle_events = max(event.time for event in obstacle_events)
    else:
        max_time_obstacle_events = MATCH_TIME
    current_obstacles = list(filter(lambda event: max_time_obstacle_events - 1 <= event.time <= max_time_obstacle_events, obstacle_events))
    for event in current_obstacles:
        if event.place is None or event.number is None:
            raise ValueError()
        state.obstacles.append((event.place[0], event.place[1], event.number))
    return state

class ReplayUI:
    screen: pygame.Surface
    slider: Slider
    slider_value: TextBox
    play_pause_button: Button

    replay_events: list[ReplayEvent] = []
    state: ReplayState
    is_playing = False
    time: float = 0
    start_playing_real_time: float = 0

    def __init__(self, window_name: str):
        self.window_name = window_name

    def rotate_image_around_center(self, image: pygame.Surface, x: float, y: float, angle: float) -> None:
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = (x,y)).center)
        self.screen.blit(rotated_image, new_rect)

    def update_events(self, replay_events: list[ReplayEvent]):
        self.replay_events = replay_events
        self.state = compute_state(self.replay_events, self.time)

    def start_ui(self):
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.slider = Slider(self.screen, PLAYING_AREA_WIDTH/MM_TO_PIXEL_DIVIDER + MARGIN, MARGIN, SLIDER_WIDTH, 10, min=0, max=100, step=0.25, initial=0)
        self.slider_value = TextBox(self.screen, PLAYING_AREA_WIDTH/MM_TO_PIXEL_DIVIDER + MARGIN, 2*MARGIN + 10, SLIDER_WIDTH, 30, fontSize=20, onSubmit=self.change_time)
        self.slider_value.setText(self.slider.getValue())
        self.play_pause_button = Button(self.screen, PLAYING_AREA_WIDTH / MM_TO_PIXEL_DIVIDER + MARGIN, 80, SLIDER_WIDTH, 20, text="Play / Pause", onClick=self.press_play_pause_button)

        pygame.display.set_caption(self.window_name)

        background = pygame.image.load(os.path.join("res", "background.png"))
        robot = pygame.image.load(os.path.join("res", "robot.png"))
        previous_time: float = 0

        self.state = compute_state(self.replay_events, self.time)

        show_ui = True

        while show_ui:
            if self.is_playing:
                real_time = time_library.time()
                self.time = min(100, round(real_time - self.start_playing_real_time, 2))
                self.slider.setValue(self.time)
            else:  
                self.time = float(self.slider.getValue())

            if previous_time != self.time:
                previous_time = self.time
                self.slider_value.setText(self.time)
                self.state = compute_state(self.replay_events, self.time)
                
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    show_ui = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(background, (0, 0))

            if self.state.robot_position is not None:
                self.rotate_image_around_center(robot, self.state.robot_position[0] / MM_TO_PIXEL_DIVIDER - 41, (PLAYING_AREA_DEPTH - self.state.robot_position[1]) / MM_TO_PIXEL_DIVIDER - 41, self.state.robot_position[2] * 180 / math.pi)

            if self.state.robot_goal is not None:
                pygame.draw.circle(self.screen, (0, 255, 0), (self.state.robot_goal[0] / MM_TO_PIXEL_DIVIDER, (PLAYING_AREA_DEPTH - self.state.robot_goal[1]) / MM_TO_PIXEL_DIVIDER), 10)

            if len(self.state.robot_path) > 0:
                pairs = pairwise(self.state.robot_path)
                for pair in pairs:
                    pygame.draw.line(
                        self.screen, 
                        (0, 0, 255), 
                        (pair[0][0] / MM_TO_PIXEL_DIVIDER, (PLAYING_AREA_DEPTH - pair[0][1]) / MM_TO_PIXEL_DIVIDER),
                        (pair[1][0] / MM_TO_PIXEL_DIVIDER, (PLAYING_AREA_DEPTH - pair[1][1]) / MM_TO_PIXEL_DIVIDER)
                    )

            for obstacle in self.state.obstacles:
                pygame.draw.circle(self.screen, (125, 125, 125), (obstacle[0] / MM_TO_PIXEL_DIVIDER, (PLAYING_AREA_DEPTH - obstacle[1]) / MM_TO_PIXEL_DIVIDER), obstacle[2] / 10)
            
            pygame_widgets.update(events)
            pygame.display.update()


    def press_play_pause_button(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.start_playing_real_time = time_library.time() - self.time
            self.slider.disable()
            self.slider_value.disable()
        else:
            self.slider.enable()
            self.slider_value.enable()

    def change_time(self):
        self.slider.setValue(float(self.slider_value.getText()))
