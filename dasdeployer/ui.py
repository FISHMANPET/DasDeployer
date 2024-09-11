from dataclasses import dataclass, field
from gpiozero import LEDBoard, ButtonBoard, Button
from lcd import LCD_HD44780_I2C
from rgb import RGBButton

@dataclass
class UiElements:
    switch_lights: LEDBoard
    switches: ButtonBoard
    toggle_lights: LEDBoard
    toggles: ButtonBoard
    keys: ButtonBoard
    lcd: LCD_HD44780_I2C
    rgb_matrix: RGBButton | None
    big_button: Button
    all_leds: LEDBoard = field(init=False)

    def __post_init__(self):
        self.all_leds = LEDBoard(self.switch_lights, self.toggle_lights)
