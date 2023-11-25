from enum import Enum


MATCH_TIME: int = 100 # Duration of a match
PLAYING_AREA_WIDTH = 3000
PLAYING_AREA_DEPTH = 2000
D_STAR_FACTOR = 50
ROBOT_WIDTH = 325
ROBOT_DEPTH = 155
mock_robot = False # Use real serial or mock it

class Side(Enum):
    BLUE = 0
    YELLOW = 1
