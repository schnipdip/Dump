import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from time import sleep

from linux.dumper.output.Output import Output


def init_lcd():
    """
        Params: lcd_columns - number of columns the LCD Screen has (int)
                lcd_rows    - number of rows the LCD Screen has (int)
                i2c         - calling i2c program
                lcd         - setting lcd screen
        Returns: lcd
    """

    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    return lcd


class LcdOutput(Output):

    def __init__(self):
        self.lcd = init_lcd()

    def print(self, message, timeout: float = .5):
        self.lcd.clear()
        self.lcd.message = "Detecting USBs"
        sleep(timeout)
