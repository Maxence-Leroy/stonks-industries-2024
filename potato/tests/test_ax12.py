import serial
import time

serial = serial.Serial(
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

serial.write(b'\xff\xff\x01\x04\x02\x2B\x01\xcc')
serial.flush()
time.sleep(1)
res = serial.read_all()
if res:
    print(res.decode())