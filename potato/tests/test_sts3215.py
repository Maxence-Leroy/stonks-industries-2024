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
        p = position.to_bytes(2, 'big', signed=True)
        self.send_command(id, b'\x03', [b'\x2A', p[0:1], p[1:2]])

    def speed_to_bytes(self, speed: int) -> bytes:
        if speed < 0:
            s = (-speed + 1024).to_bytes(2, 'little')
        else:
            s = speed.to_bytes(2, 'little')
        return s

    def set_speed(self, id: int, speed: int) -> None:
        s = self.speed_to_bytes(speed)
        self.send_command(id, b'\x03', [b'\x2C', s[0:1], s[1:2]])

    def set_speed_mutliples(self, ids: list[int], speed: int) -> None:
        s = self.speed_to_bytes(speed)
        parameters: list[bytes] = [b'\x2C', b'\x02']

        for id in ids:
            parameters += [id.to_bytes(1, 'little')]
            parameters += [s[0:1], s[1:2]]
        self.send_command(254, b'\x83', parameters)
        self.read_ignore_previous_command()

    def set_mode(self, id: int, mode: int) -> None:
        if mode < 0 or mode > 3:
            raise ValueError()
        self.send_command(id, b'\x03', [b'\x21', mode.to_bytes(1, 'little')])

    def set_eeprom_lock(self, id: int, lock: bool) -> None:
        self.send_command(id, b'\x03', [b'\x30', b'\x01' if lock else b'\x00'])

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
        self.serial.flush()

def change_id(sts: STS3215, old_id: int, new_id: int):
    sts.set_eeprom_lock(old_id, False)
    time.sleep(1)
    sts.change_id(old_id, new_id)
    time.sleep(1)
    sts.set_eeprom_lock(new_id, True)

def switch_to_continous_mode(sts: STS3215, id: int):
    sts.set_mode(id, 2)
    print(sts.read_ignore_previous_command())
    sts.set_speed(id, -1000)
    print(sts.read_ignore_previous_command())
    time.sleep(5)
    sts.set_speed(id, 1000)
    sts.read_ignore_previous_command()
    time.sleep(5)
    sts.set_mode(id, 0)
    sts.read_ignore_previous_command()
    sts.set_speed(id, 0)
    sts.read_ignore_previous_command()

def turn_multiples(sts: STS3215, ids: list[int]):
    for id in ids:
         sts.set_mode(id, 2)
    sts.set_speed_mutliples(ids, 1000)
    time.sleep(5)
    sts.set_speed_mutliples(ids, -1000)
    time.sleep(5)
    sts.set_speed_mutliples(ids, 0)
    for id in ids:
        sts.set_mode(id, 0)

def start():
    sts = STS3215()
    sts.set_mode(1, 2)
    sts.set_speed_mutliples([1], -1000)

def stop():
    sts = STS3215()
    sts.set_mode(1, 2)
    sts.set_speed_mutliples([1], 0)

def init():
    sts = STS3215()
    sts.send_command(10, b'\x03', [b'\x09', b'\x00', b'\x00', b'\x00', b'\x00'])

if __name__ == "__main__":
    sts = STS3215()
    # init()
    # time.sleep(4)

    # sts.send_command(10, b'\x03', [b'\x028', b'\x01'])
    # sts.move(10, 200)
    # time.sleep(2)
    # sts.move(10, 20)
    new_id = 10

    # print("Change id")
    # change_id(sts, 1, new_id)
    # time.sleep(5)

    # print("Debrick")
    # sts.set_eeprom_lock(new_id, False)
    # time.sleep(0.5)
    # sts.send_command(new_id, b'\x03', [b'\x12', b'\x01'])
    # time.sleep(0.5)
    # sts.set_eeprom_lock(new_id, True)
    # time.sleep(5)

    for dest in range(-1000, 1000, 20):
        print(dest)
        sts.move(new_id, dest)
        time.sleep(0.3)


    # print("Move 1")
    # sts.move(new_id, 200)
    # time.sleep(3)
    # print("Move 2")
    # sts.move(new_id, 2000)
    # time.sleep(3)



