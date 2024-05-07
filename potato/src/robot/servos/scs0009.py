from src.robot.servos.servo import Servo

class SCS0009(Servo):
    def _convert_16bits_to_bytes(self, value: int) -> bytes:
        return value.to_bytes(2, 'big')
    
class MockSCS0009(SCS0009):
    def __init__(self):
        super().__init__(None) # type: ignore

    def move_continuous(self, ids: list[int], speed: int) -> None:
        pass

    async def move_to_position(self, ids: list[int], positions: list[int], wait_for_finish: bool) -> None:
        pass