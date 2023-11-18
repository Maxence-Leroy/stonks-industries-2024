from dataclasses import dataclass
import math
import os
import time as time_library
from typing import Optional
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import sys

from src.constants import PLAYING_AREA_DEPTH, PLAYING_AREA_WIDTH
from src.helpers.pairwise import pairwise
from src.replay.base_classes import ReplayEvent, EventType
from src.replay.load_replay import load_replay

is_playing = False
DIVIDER = 4
time: float = 0
start_playing_real_time: float = 0

@dataclass
class State:
    robot_path: list[tuple[float, float, float]]
    robot_position: Optional[tuple[float, float, float]] = None
    robot_goal: Optional[tuple[float, float, float]] = None

def compute_state(events: list[ReplayEvent], time: float) -> State:
    events.sort(key=lambda event: event.time)
    state = State([])
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
    return state

def blitRotateCenter(surf: pygame.Surface, image: pygame.Surface, x: float, y: float, angle: float) -> None:
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = (x,y)).center)
    surf.blit(rotated_image, new_rect)



def main():
    global time
    done = False
    if len(sys.argv) != 2:
        raise ValueError()
    file_path = sys.argv[1]
    replay_events = load_replay(file_path)

    pygame.init()

    def press_button():
        global is_playing
        global start_playing_real_time
        is_playing = not is_playing
        if is_playing:
            start_playing_real_time = time_library.time()
            slider.disable()
            slider_value.disable()
        else:
            slider.enable()
            slider_value.enable()

    SLIDER_WIDTH = 100
    MARGIN = 10
    WINDOW_SIZE = [PLAYING_AREA_WIDTH / DIVIDER + 2 * MARGIN + SLIDER_WIDTH, PLAYING_AREA_DEPTH / DIVIDER]

    def change_time():
        slider.setValue(float(slider_value.getText()))

    screen = pygame.display.set_mode(WINDOW_SIZE)
    slider = Slider(screen, PLAYING_AREA_WIDTH/DIVIDER + MARGIN, MARGIN, SLIDER_WIDTH, 10, min=0, max=100, step=0.25, initial=0)
    slider_value = TextBox(screen, PLAYING_AREA_WIDTH/DIVIDER + MARGIN, 2*MARGIN + 10, SLIDER_WIDTH, 30, fontSize=20, onSubmit=change_time)
    slider_value.setText(slider.getValue())
    button = Button(screen, PLAYING_AREA_WIDTH / DIVIDER + MARGIN, 80, SLIDER_WIDTH, 20, text="Play / Pause", onClick=press_button)
    pygame.display.set_caption(f"Replay {file_path}")
    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join("res", "background.png"))
    robot = pygame.image.load(os.path.join("res", "robot.png"))
    previous_time: float = 0
    
    state = compute_state(replay_events, time)

    while not done:
        if is_playing:
            real_time = time_library.time()
            time = min(100, round(real_time - start_playing_real_time, 2))
            slider.setValue(time)
        else:  
            time = float(slider.getValue())

        if previous_time != time:
            previous_time = time
            slider_value.setText(time)
            state = compute_state(replay_events, time)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True

        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        if state.robot_position is not None:
            blitRotateCenter(screen, robot, state.robot_position[0] / DIVIDER - 41, (PLAYING_AREA_DEPTH - state.robot_position[1]) / DIVIDER - 41, state.robot_position[2] * 180 / math.pi)
        if state.robot_goal is not None:
            pygame.draw.circle(screen, (0, 255, 0), (state.robot_goal[0] / DIVIDER, (PLAYING_AREA_DEPTH - state.robot_goal[1]) / DIVIDER), 10)
        if len(state.robot_path) > 0:
            pairs = pairwise(state.robot_path)
            for pair in pairs:
                pygame.draw.line(
                    screen, 
                    (0, 0, 255), 
                    (pair[0][0] / DIVIDER, (PLAYING_AREA_DEPTH - pair[0][1]) / DIVIDER),
                    (pair[1][0] / DIVIDER, (PLAYING_AREA_DEPTH - pair[1][1]) / DIVIDER)
                )
        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == "__main__":
    main()