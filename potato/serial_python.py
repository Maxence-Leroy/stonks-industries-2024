import time
import serial
import gpiod

if __name__ == '__main__':
    ser = serial.Serial(
        port = '/dev/ttyAML6',
        baudrate = 115200,
        timeout = 1,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        xonxoff = False,
        rtscts = False,
        dsrdtr = False,
        write_timeout = 1.0
    )
    time.sleep(1)
    ser.write('bon1jour\n'.encode('utf-8'))
    ser.flush()
    time.sleep(1)
    ser.close()
    print("Done")
#     chip = gpiod.chip("gpiochip1")
#     line = chip.get_line(15)
#     config = gpiod.line_request()
#     config.consumer = "Consumer"
#     config.request_type = gpiod.line_request.DIRECTION_OUTPUT
#     line.request(config)
#     
#     for i in range(0,10):
#         line.set_value(0)
#         time.sleep(1.0)
#         line.set_value(1)
#         time.sleep(1.0)
