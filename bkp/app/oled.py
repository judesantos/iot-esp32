# oled convencinec class to print text in screen

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import time

#
# display preoprties
#
MAX_LINES = const(6)
MAX_CHARS_PER_LINE = const(16)

SCL_PINOUT = const(15)
SDA_PINOUT = const(4)
# values are in pixels
OLED_WIDTH_PIXELS = const(128)
OLED_HEIGHT_PIXELS = const(64)
LEFT_MARGIN = const(0)
LINE_HEIGHT_PIXELS = const(9)
START_TOP = const(0)

# private OLED class implementation
class _OLED:

    def __init__(self):
        self.nextLinePosPx = 0
        # initialize OLED device
        rst = Pin(16, Pin.OUT)
        rst.value(1)

        scl = Pin(SCL_PINOUT, Pin.OUT, Pin.PULL_UP)
        sda = Pin(SDA_PINOUT, Pin.OUT, Pin.PULL_UP)

        i2c = I2C(scl=scl, sda=sda, freq=450000)
        self.oled = SSD1306_I2C(OLED_WIDTH_PIXELS, OLED_HEIGHT_PIXELS, i2c, addr=0x3c)

        self.oled.fill(0)

    def reset(self):
        self.oled.fill(0)
        self.nextLinePosPx = START_TOP
        self.currLineCount = 0

    def line(self, x1, y1, x2, y2):
        self.oled.line(xy, y1, x2, y2)

    def pixel(self, x, y):
        self.oled.pixel(x, y)

    def rect(self, x, y, w, h, c=None):
        if None == c:
            self.oled.rect(x, y, w, h)
        else:
            self.oled.fill_rect(x, y, w, h, c)

    def textPosV(self, text, x=LEFT_MARGIN, y=-1):
        if not -1 == y:
            self.nextLinePosPx = y * LINE_HEIGHT_PIXELS
        else:
            self.nextLinePosPx += LINE_HEIGHT_PIXELS
        self.rect(x, self.nextLinePosPx, OLED_WIDTH_PIXELS, LINE_HEIGHT_PIXELS, 0) 
        self.oled.text(text, x, self.nextLinePosPx)
        self.oled.show()

    def text(self, text, lastPosY=False):
        # set next line position
        if False == lastPosY: 
            self.nextLinePosPx += LINE_HEIGHT_PIXELS
        else:
            self.rect(LEFT_MARGIN, self.nextLinePosPx, OLED_WIDTH_PIXELS, LINE_HEIGHT_PIXELS, 0) 
        self.oled.text(text, LEFT_MARGIN, self.nextLinePosPx)
        self.oled.show()

    def show(self):
        self.oled.show()

    def vscrollOut(self, speed):
        for i in range((OLED_HEIGHT_PIXELS+1)/speed):
            for j in range(OLED_WIDTH_PIXELS):
                self.oled.pixel(j, i, 0)
            self.oled.scroll(0, -speed)
            self.oled.show()

# public inteface - OLED singleton 
class OLED(_OLED):

    __instance = None

    @staticmethod
    def instance():
        if OLED.__instance is None:
            OLED.__instance = _OLED() 
        return OLED.__instance

