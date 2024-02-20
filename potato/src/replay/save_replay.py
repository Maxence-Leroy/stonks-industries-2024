import dataclasses
from io import TextIOWrapper
import json
import os
import time
from typing import Optional
import socket

from src.replay.base_classes import ReplayEvent, EventType

start_match: float = 0
save_replay: bool = True
file: Optional[TextIOWrapper] = None

send_teleplot: bool = True
teleplot_addr = ("127.0.0.1",47269)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
previous_teleplot: float = 0
send_maxplot: bool = True
maxplot_addr = ("192.168.189.149", 53572)


def start_replay():
    global start_match
    start_match = time.time()

def open_replay_file(file_name: str = ""):
    global file
    if save_replay:
        filename = f"replay_logs/{file_name}{str(int(time.time()))}.log"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, "w")

def log_replay(event: ReplayEvent):
    current_time = time.time() - start_match if start_match != 0 else 0

    event.time = current_time
    event_dict = dataclasses.asdict(event)
    event_json = json.dumps(event_dict)

    if save_replay and file is not None:
        file.write(event_json)
        file.write("\n")
        file.flush()

    if send_teleplot:
        global previous_teleplot
        event_name = event.event.string_name()
        event_place = event.place
        if event_name != "" and event_place is not None:
            if event.event == EventType.ROBOT_POSITION and current_time * 1000 < previous_teleplot + 50:
                return
            previous_teleplot = current_time * 1000
            msg = f"{event_name}:{event_place[0]}:{event_place[1]}:{current_time * 1000}|xy"
            sock.sendto(msg.encode(), teleplot_addr)
    
    if send_maxplot:
        sock.sendto(event_json.encode(), maxplot_addr)

