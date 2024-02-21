import json
import socket
import sys
import threading

from src.replay.base_classes import ReplayEvent
from src.replay.load_replay import load_replay, event_decoder
from src.replay.replay_ui import ReplayUI

UDP_PORT = 53572

ui: ReplayUI

def main():
    global ui

    if len(sys.argv) < 2:
        raise ValueError()
    type = sys.argv[1]

    if type == "file":
        if len(sys.argv) != 3:
            raise ValueError()
        file_path = sys.argv[2]
        ui = ReplayUI(f"Replay {file_path}")
        replay_events = load_replay(file_path)
        ui.update_events(replay_events)
        ui.start_ui()
    elif type == "live":
        ui = ReplayUI("Live feed")
        socket_thread = threading.Thread(target=udp_server)
        socket_thread.start()
        ui.start_ui()
    else:
        raise ValueError()
    
def udp_server():
    global ui

    events: list[ReplayEvent] = []

    sock = socket.socket(
        socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
    
    sock.bind(("192.168.189.149", UDP_PORT))

    while True:
        data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
        try:
            event = json.loads(data.decode(), object_hook=event_decoder)
            events.append(event)
            ui.update_events(events)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()