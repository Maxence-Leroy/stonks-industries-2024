from enum import Enum


MATCH_TIME: int = 100 # Duration of a match
PLAYING_AREA_WIDTH = 3000
PLAYING_AREA_DEPTH = 2000
D_STAR_FACTOR = 50
ROBOT_WIDTH = 325
ROBOT_DEPTH = 155
mock_robot = True # Use real serial or mock it

ID_SERVO_PLANT_LEFT = 5
ID_SERVO_PLANT_MID = 7
ID_SERVO_PLANT_RIGHT = 6

class PlantCanal(Enum):
    LEFT = 0
    MID = 1
    RIGHT = 2

    def servo_id(self) -> int:
        if self == PlantCanal.LEFT:
            return ID_SERVO_PLANT_LEFT
        elif self == PlantCanal.MID:
            return ID_SERVO_PLANT_MID
        else:
            return ID_SERVO_PLANT_RIGHT
        
PLANT_DETECTION_THRESHOLD = 500
MARGIN_PLANT = 200
MARGIN__POT = 200
MARGIN_PLANTER = 200

class Side(Enum):
    BLUE = 0
    YELLOW = 1
