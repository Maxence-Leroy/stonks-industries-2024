import serial
import time

class STS3215:
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

    def change_id(self, id: int, new_id: int) -> None:
        if new_id < 0 or new_id > 0XFD:
            raise ValueError()
        self.send_command(id, b'\x03', [b'\x05', new_id.to_bytes(1, 'little')])

    def move(self, id: int, position: int) -> None:
        p = position.to_bytes(2, 'little', signed=True)
        self.send_command(id, b'\x03', [b'\x2A', p[0:1], p[1:2]])

    def set_eeprom_lock(self, id: int, lock: bool) -> None:
        self.send_command(id, b'\x03', [b'\x37', b'\x01' if lock else b'\x00'])

    def get_voltage_limit(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x0E', b'\x02'])
        return self.read_ignore_previous_command()
    
    def get_minimum_angle(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x09', b'\x02'])
        return self.read_ignore_previous_command()
    
    def get_maximum_angle(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x0B', b'\x02'])
        return self.read_ignore_previous_command()
    
    def get_current_position(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x38', b'\x02'])
        return self.read_ignore_previous_command()

    def get_current_voltage(self, id: int) -> bytes:
        self.send_command(id, b'\x02', [b'\x3E', b'\x01'])
        return self.read_ignore_previous_command()
    
    def read_ignore_previous_command(self) -> bytes:
        time.sleep(0.1)
        res = self.serial.read_all()
        if not res:
            return b''
        res = res[len(self.last_command):]
        return res
    
    def set_id(self, old_id: int, new_id: int) -> None:
        if new_id < 0 or new_id > 0XFD:
            raise ValueError()
        new_id_bytes = new_id.to_bytes(1, 'little')
        self.send_command(old_id, b'\x03', [b'\x05', new_id_bytes])


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
        full_command += checksum_bytes

        self.last_command = full_command
        self.serial.write(full_command)
        self.serial.flush()

if __name__ == "__main__":
    sts = STS3215()
    sts.set_eeprom_lock(1, False)
    print(sts.read_ignore_previous_command())
    sts.change_id(1, 2)
    print(sts.read_ignore_previous_command())
    sts.set_eeprom_lock(2, True)
    print(sts.read_ignore_previous_command())
