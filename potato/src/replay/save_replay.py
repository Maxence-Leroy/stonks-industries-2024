import dataclasses
from io import TextIOWrapper
import json
import os
import time
from typing import Optional

from src.replay.base_classes import ReplayEvent

start_match: float = 0
save_replay: bool = True
file: Optional[TextIOWrapper] = None

def start_replay():
    global start_match
    start_match = time.time()

def open_replay_file():
    global file
    if save_replay:
        filename = f"replay/{str(int(time.time()))}.log"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, "w")

def log_replay(event: ReplayEvent):
    if save_replay and file is not None:
        current_time = time.time() - start_match if start_match != 0 else 0
        event.time = current_time
        event_dict = dataclasses.asdict(event)
        event_json = json.dumps(event_dict)
        file.write(event_json)
        file.write("\n")
        file.flush()
