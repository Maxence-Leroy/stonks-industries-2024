import asyncio
import serial
import time

class STS3215:
    CONTINOUS_MODE = 2
    DESTINATION_MODE = 0

    def __init__(self):
        self.serial = serial.Serial(
            port="/dev/ttyAML7",
            baudrate=1000000,
            timeout=10,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        self.last_command = ""

    def _move(self, id: int, position: int) -> None:
        """Move a servo to the given position"""
        p = position.to_bytes(2, 'little', signed=True)
        self._send_command(id, b'\x03', [b'\x2A', p[0:1], p[1:2]])
        self._read_ignore_previous_command()

    def _move_multiples(self, ids: list[int], positions: list[int]) -> None:
        """Move multiple servos to the given position"""
        parameters: list[bytes] = [b'\x2A', b'\x02']

        if len(positions) != len(ids):
            raise ValueError()

        for i in range(0, len(ids)):
            parameters += [ids[i].to_bytes(1, 'little')]
            p = positions[i].to_bytes(2, 'little', signed=True)
            parameters += [p[0:1], p[1:2]]
        self._send_command(254, b'\x83', parameters)
        self._read_ignore_previous_command()

    def _speed_to_bytes(self, speed: int) -> bytes:
        """Convert a speed int (between -1000 and 1000)"""
        s = abs(speed).to_bytes(2, 'little', signed=True)
        if speed < 0:
            sign = (1<<15).to_bytes(2, 'little')
            s = (int.from_bytes(s, 'little') | int.from_bytes(sign, 'little')).to_bytes(2, 'little')
        return s

    def _set_speed(self, id: int, speed: int) -> None:
        """Set speed in continuous mode for one servo"""
        s = self._speed_to_bytes(speed)
        self._send_command(id, b'\x03', [b'\x2C', s[0:1], s[1:2]])
        self._read_ignore_previous_command()

    def _set_speed_mutliples(self, ids: list[int], speed: int) -> None:
        """Set speed in continuous mode for multiple servos"""
        s = self._speed_to_bytes(speed)
        parameters: list[bytes] = [b'\x2C', b'\x02']

        for id in ids:
            parameters += [id.to_bytes(1, 'little')]
            parameters += [s[0:1], s[1:2]]
        self._send_command(254, b'\x83', parameters)
        self._read_ignore_previous_command()

    def _set_mode(self, id: int, mode: int) -> None:
        """Change moving mode"""
        if mode < 0 or mode > 3:
            raise ValueError()
        self._send_command(id, b'\x03', [b'\x21', mode.to_bytes(1, 'little')])
        self._read_ignore_previous_command()

    def _is_moving(self, id: int) -> bool:
        """Check if the servo is still moving"""
        self._send_command(id, b'\x02', [b'\x42', b'\x01'])
        res = self._read_ignore_previous_command()
        return len(res) == 0 or res[5] > 0
    
    def _read_ignore_previous_command(self) -> bytes:
        time.sleep(0.1)
        res = self.serial.read_all()
        if not res:
            return b''
        res = res[len(self.last_command):]
        return res

    def _send_command(self, id: int, command: bytes, parameters: list[bytes]) -> None:
        if id < 0 or id > 0XFE:
            raise ValueError()
        id_bytes = id.to_bytes(1, 'little')
        length = len(parameters) + 2
        length_bytes = length.to_bytes(1, 'little')
        sum = id + length + int.from_bytes(command, 'little')
        for parameter in parameters:
            sum += int.from_bytes(parameter, 'little')
        checksum = (~(sum))&0xff
        full_command = b'\xFF\xFF' + id_bytes + length_bytes + command
        for parameter in parameters:
            full_command += parameter
        checksum_bytes = checksum.to_bytes(1, 'little')
        full_command += checksum_bytes

        self.last_command = full_command
        self.serial.write(full_command)

    def move_continuous(self, ids: list[int], speed: int):
        """Move multiple servos in continuous mode. Speed can be between -1000 and 1000, 0 is stop."""
        for id in ids:
            self._set_mode(id, self.CONTINOUS_MODE)
        
        self._set_speed_mutliples(ids, speed)

    async def move_to_position(self, ids: list[int], positions: list[int], wait_for_finish: bool) -> None:
        """
        Move multiple servos to set position. Ids and position lists must be same size.
        Positions must be between 0 and 4000.
        """
        for id in ids:
            self._set_mode(id, self.DESTINATION_MODE)
        self._move_multiples(ids, positions)

        if wait_for_finish:
            have_all_finished = False
            while not have_all_finished:
                have_all_finished = True
                for id in ids:
                    if self._is_moving(id):
                        have_all_finished = False
                        break
                await asyncio.sleep(0.1)

        await asyncio.sleep(0.1)
        return
