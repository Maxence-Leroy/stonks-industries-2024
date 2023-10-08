class PlayingArea:
    def get_next_pot(self) -> tuple[float, float, float]:
        return (0, 0, 0)

    def get_next_plant(self) -> tuple[float, float, float]:
        return (1, 1, 1)

    def get_next_planter(self) -> tuple[float, float, float]:
        return (2, 2, 2)

    def get_solar_pannel_begin(self) -> tuple[float, float, float]:
        return (4, 4, 4)

    def get_solar_pannel_end(self) -> tuple[float, float, float]:
        return (10, 10, 10)

    def get_end_area(self) -> tuple[float, float, float]:
        return (100, 100, 100)
