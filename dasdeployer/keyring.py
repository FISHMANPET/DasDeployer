from rgb import Color, RGBButton
from gpiozero import ButtonBoard
import time

keys = ButtonBoard(one=14, two=15)

color = Color.GREEN

rgbmatrix = RGBButton()
rgbmatrix.fill(color)
print("fill")
time.sleep(2)
rgbmatrix.flashKey1(color, .5)
rgbmatrix.flashKey2(color, .5)
# rgbmatrix.flashRing(Color.YELLOW, .5)
print("flash")
time.sleep(2)
rgbmatrix.pulseKey1(color, .5)
rgbmatrix.pulseKey2(color, .5)
# rgbmatrix.pulseRing(Color.YELLOW, .5)
print("pulse")
time.sleep(2)
rgbmatrix.chaseKey1(color)
rgbmatrix.chaseKey2(color)
print("chase")
# time.sleep(25)
# rgbmatrix.unicornRing(5)
# print("unicorn")
# time.sleep(10)
# rgbmatrix.chaseKey1(Color.YELLOW, 10)
# time.sleep(5)
# rgbmatrix.flashButton(Color.BLUE, 5)
# print("fill button")
# time.sleep(25)
# rgbmatrix.fillButton((51, 51, 51))
# time.sleep(5)
# rgbmatrix.stopKey1()
# print("stop key")
# time.sleep(1)
# rgbmatrix.stopKey1()
keys.one.wait_for_press()
print("one turned")
keys.two.wait_for_press()
print("two turned")
rgbmatrix.off()
print("off")
