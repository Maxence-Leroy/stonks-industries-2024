class RobotState():
    def __init__(self) -> None:
        self.score = 0
        self.plants_left = 0
        self.plants_mid = 0
        self.plants_right = 0
        self.plant_canal_running: list[int] = []
        self.pots = 0
        self.plants_in_pots = 0