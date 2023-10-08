from enum import Enum

from src.playing_area import PlayingArea


class Location:
    def getLocation(self) -> tuple[float, float, float]:
        raise NotImplementedError()


class Coordinates(Location):
    def __init__(self, x: float, y: float, theta: float) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self) -> str:
        return f"(x: {self.x}, y: {self.y}, θ: {self.theta})"

    def getLocation(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.theta)


ImportantLocation = Enum(
    "ImportantLocation",
    ["POT", "PLANT", "PLANTER", "SOLAR_PANNEL_BEGIN", "SOLAR_PANNEL_END", "END_AREA"],
)


class BestAvailable(Location):
    def __init__(self, location: ImportantLocation, playing_area: PlayingArea) -> None:
        super().__init__()
        self.location = location
        self.playing_area = playing_area

    def __str__(self) -> str:
        return f'Next {str(self.location).replace("_", " ").lower()}'

    def getLocation(self) -> tuple[float, float, float]:
        match self.location:
            case ImportantLocation.POT:
                return self.playing_area.get_next_pot()
            case ImportantLocation.PLANT:
                return self.playing_area.get_next_plant()
            case ImportantLocation.PLANTER:
                return self.playing_area.get_next_planter()
            case ImportantLocation.SOLAR_PANNEL_BEGIN:
                return self.playing_area.get_solar_pannel_begin()
            case ImportantLocation.SOLAR_PANNEL_END:
                return self.playing_area.get_solar_pannel_end()
            case ImportantLocation.END_AREA:
                return self.playing_area.get_end_area()
