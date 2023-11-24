import serial
import time

class AX12:
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
            dsrdtr=False,
            write_timeout=1.0,
        )
        self.last_command = ""

    def move(self, id: int, position: int) -> None:
        p = [position&0xff, position>>8]
        p = list(map(lambda a: a.to_bytes(1, 'little'), p))
        self.send_command(id, b'\x03', [b'\x1E'] + p)

    def send_command(self, id: int, command: bytes, parameters: list[bytes]) -> None:
        if id < 0 or id > 0XFD:
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
        full_command += checksum.to_bytes(1, 'little')

        self.last_command = full_command
        self.serial.write(full_command)
        self.serial.flush()

if __name__ == "__main__":
    ax = AX12()
    ax.move(1, 500)