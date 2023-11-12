from src.path.angle import Angle

class PlayingArea:
    """Class represenging the playing area.
    
    TODO: Add state
    """
    def get_next_pot(self) -> tuple[float, float, Angle]:
        return (0, 0, Angle(0))

    def get_next_plant(self) -> tuple[float, float, Angle]:
        return (1, 1, Angle(1))

    def get_next_planter(self) -> tuple[float, float, Angle]:
        return (2, 2, Angle(2))

    def get_solar_pannel_begin(self) -> tuple[float, float, Angle]:
        return (4, 4, Angle(4))

    def get_solar_pannel_end(self) -> tuple[float, float, Angle]:
        return (10, 10, Angle(10))

    def get_end_area(self) -> tuple[float, float, Angle]:
        return (100, 100, Angle(100))
    

playing_area = PlayingArea() # Singleton
