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
        print(p)
        self.send_command(id, b'\x03', [b'\x1E'] + p)

    def get_voltage_limit(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x0C', b'\x02'])
        return self.read_ignore_previous_command()
    
    def get_current_position(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x24', b'\x02'])
        return self.read_ignore_previous_command()

    def get_current_voltage(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x2a', b'\x01'])
        return self.read_ignore_previous_command()
    
    def read_ignore_previous_command(self) -> bytes:
        time.sleep(0.1)
        res = self.serial.read_all()
        if not res:
            return b''
        res = res[len(self.last_command):]
        return res


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
        checksum_bytes = checksum.to_bytes(1, 'little')
        print(checksum_bytes)
        full_command += checksum_bytes

        self.last_command = full_command
        print(full_command)
        self.serial.write(full_command)
        self.serial.flush()

if __name__ == "__main__":
    ax = AX12()
    print("Current voltage")
    print(ax.get_current_voltage(1))
    print("Voltage limit")
    print(ax.get_voltage_limit(1))
    print("Move to 1000")
    ax.move(1, 1000)
    print(ax.read_ignore_previous_command())
    time.sleep(1)
    print("Current position")
    print(ax.get_current_position(1))
