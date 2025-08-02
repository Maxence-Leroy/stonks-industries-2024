from src.robot.servos.servo import Servo

class STS3215(Servo):
    def _convert_16bits_to_bytes(self, value: int) -> bytes:
        return value.to_bytes(2, 'little')
    
    def _speed_to_bytes(self, speed: int) -> bytes:
        if speed < 0:
            s = (-speed + 1024).to_bytes(2, 'little')
        else:
            s = speed.to_bytes(2, 'little')
        return s
    
class MockSTS3215(STS3215):
    def __init__(self):
        super().__init__(None) # type: ignore

    def move_continuous(self, ids: list[int], speed: int) -> None:
        pass

    async def move_to_position(self, ids: list[int], positions: list[int], wait_for_finish: bool) -> None:
        pass