import json
from typing import Any

from src.replay.base_classes import ReplayEvent, EventType

def event_decoder(event_dict: dict[str, Any]) -> ReplayEvent:
    return ReplayEvent(
        event=EventType(event_dict["event"]),
        place=tuple[float, float, float](event_dict["place"]),
        number=event_dict["number"],
        time=event_dict["time"]
    )

def load_replay(file: str) -> list[ReplayEvent]:
    events: list[ReplayEvent] = []
    with open(file, "r") as f:
        for line in f.readlines():
            event = json.loads(line, object_hook=event_decoder)
            events.append(event)
    return events