import sys

from src.replay.load_replay import load_replay
from src.replay.replay_ui import ReplayUI


def main():
    if len(sys.argv) != 2:
        raise ValueError()
    file_path = sys.argv[1]
    ui = ReplayUI(f"Replay {file_path}")
    replay_events = load_replay(file_path)
    ui.update_events(replay_events)
    ui.start_ui()

if __name__ == "__main__":
    main()