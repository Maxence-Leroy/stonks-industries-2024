# SPDX-FileCopyrightText: 2014 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import busio
from PIL import Image, ImageFont, ImageDraw
import adafruit_ssd1306
from adafruit_blinka.microcontroller.generic_linux.i2c import I2C as _I2C
import subprocess

class PotatoI2C(busio.I2C):
    def __init__(self, i2cId: int):
        self._i2c = _I2C(i2cId)


# Create the I2C interface.
i2c = PotatoI2C(1)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Note you can change the I2C address, or add a reset pin:
# disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c, reset=reset_pin)

# Clear display.
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.load_default(size = 15)

cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )

draw.text((0, 0),f"IP :\n{IP.decode()}", font=font, fill=255)

disp.image(image)

#image = Image.open("/home/minotaure/Documents/stonks-industries-2024/potato/tests/joy-it.jpg").convert("1")
# Display image.
# disp.image(image)
disp.show()