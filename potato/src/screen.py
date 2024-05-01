import busio
from PIL import Image, ImageFont, ImageDraw
import adafruit_ssd1306
from adafruit_blinka.microcontroller.generic_linux.i2c import I2C as _I2C
from typing import Optional
import time
from src.logging import logging_error

class PotatoI2C(busio.I2C):
    def __init__(self, i2cId: int):
        self._i2c = _I2C(i2cId)

class Screen:
    disp: Optional[adafruit_ssd1306.SSD1306_I2C]
    def __init__(self):
        i2c = PotatoI2C(1)
        try:
            self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        except Exception as _:
            logging_error("Unable to start screen")
            self.disp = None


    def show_robot_name(self):
        if self.disp is not None:
            # Clear display.
            self.disp.fill(0)
            self.disp.show()

            # Get drawing object to draw on image.
            width = self.disp.width
            height = self.disp.height
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)

            # Draw a black filled box to clear the image.
            draw.rectangle((0,0,width,height), outline=0, fill=0)

            very_small_font = ImageFont.load_default(size = 10)
            small_font = ImageFont.load_default(size = 15)
            big_font = ImageFont.load_default(size = 25)

            draw.text((18, 0), "Stonks industries", font=very_small_font, fill=255)
            draw.text((20, 12), "Copper man", font=small_font, fill=255)
            draw.text((26, 30), "Knot 0", font=big_font, fill=255)
            self.disp.image(image)
            self.disp.show()
    
    def show_time_score(self, time: float, score: int):
        if self.disp is not None:
            # Clear display.
            self.disp.fill(0)
            self.disp.show()

            # Get drawing object to draw on image.
            width = self.disp.width
            height = self.disp.height
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)

            # Draw a black filled box to clear the image.
            draw.rectangle((0,0,width,height), outline=0, fill=0)

            font = ImageFont.load_default(size = 20)

            draw.text((0, 0), f"Time : {'{:.0f}'.format(time)}s", font=font, fill=255)
            draw.text((0, 32), f"Score : {score}", font=font, fill=255)
            self.disp.image(image)
            self.disp.show()

screen = Screen() # Singleton
