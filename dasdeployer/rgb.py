# mypy: ignore-errors
"""
`dasdeployer.rgb`
====================================================

Helper class for the ring of RGB LED's that surround the big button
which are part of the same addressable matrix with the 8 RGB LED ring
inside the button.

* Author(s): Martin Woodward

**Hardware:**

"* `112mm 32 WS2812B 5050 RGB LED Ring (Adafruit Neopixel compatible) <https://amzn.to/2V5ClD0>`_"
"* `32mm 8 WS2812B 5050 RGB LED Ring (Adafruit Neopixel compatible) <https://amzn.to/2KKgZqD>`_"

**Software and Dependencies:**

* Adafruit_CircuitPython_NeoPixel https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel

"""

import neopixel
import board
import threading
from enum import Enum

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/martinwoodward/DasDeployer.git"

_PIXEL_PIN = board.D21  # NeoPixels must be connected to 10, 12, 18 or 21 to work.
_RING_PIXELS = 32
_BUTTON_PIXELS = 8
_KEY_PIXELS = 16
_RING_START = 0
_RING_END = _BUTTON_START = _RING_PIXELS
_BUTTON_END = _KEY1_START = _RING_PIXELS + _BUTTON_PIXELS
_KEY1_END = _KEY2_START = _RING_PIXELS + _BUTTON_PIXELS + _KEY_PIXELS
_KEY2_END = _NUM_PIXELS = _RING_PIXELS + _BUTTON_PIXELS + (2 * _KEY_PIXELS)
_RING_RANGE = slice(_RING_START, _RING_END)
_BUTTON_RANGE = slice(_BUTTON_START, _BUTTON_END)
_KEY1_RANGE = slice(_KEY1_START, _KEY1_END)
_KEY2_RANGE = slice(_KEY2_START, _KEY2_END)

_ORDER = neopixel.GRB  # The ones I purchased have red and green reversed


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    OFF = (0, 0, 0)


class AnimationType(Enum):
    OFF = 0
    FLASH = 1
    PULSE = 2
    CHASE = 3
    UNICORN = 4
    FILL = 5


class RGBButton():
    def __init__(self, brightness=1, ring_brightness=0.2, fps=32) -> None:
        assert 0 <= brightness <= 1
        assert 0 <= ring_brightness <= 1
        assert fps > 0
        self.brightness = brightness
        self.ring_brightness = ring_brightness
        self.delay = 1 / fps
        self.pixels = neopixel.NeoPixel(
            _PIXEL_PIN,
            _NUM_PIXELS,
            brightness=self.brightness,
            auto_write=False,
            pixel_order=_ORDER
        )
        self._animate_thread = None

    def off(self):
        self._animate_stop()
        self.pixels.fill(Color.OFF)
        self.pixels.show()

    def fill(self, color):
        self._animate_stop()
        # Ring appears brighter to the eye than the button so reduce intensity of the LEDS
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self.pixels[_RING_RANGE] = [ring_color] * _RING_PIXELS
        self.pixels[_BUTTON_RANGE] = [color] * _BUTTON_PIXELS
        self.pixels[_KEY1_RANGE] = [ring_color] * _KEY_PIXELS
        self.pixels[_KEY2_RANGE] = [ring_color] * _KEY_PIXELS
        self.pixels.show()

    def fillButton(self, color) -> None:
        self._animate_stop()
        self.pixels[_BUTTON_RANGE] = [color] * _BUTTON_PIXELS
        self.pixels.show()

    def fillRing(self, color) -> None:
        self._animate_stop()
        # Ring appears brighter to the eye than the button so reduce intensity of the LEDS
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self.pixels[_RING_RANGE] = [ring_color] * _RING_PIXELS
        self.pixels.show()

    def fillKey1(self, color):
        self._animate_stop()
        # Ring appears brighter to the eye than the button so reduce intensity of the LEDS
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self.pixels[_KEY1_RANGE] = [ring_color] * _KEY_PIXELS
        self.pixels.show()

    def fillKey2(self, color):
        self._animate_stop()
        # Ring appears brighter to the eye than the button so reduce intensity of the LEDS
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self.pixels[_KEY2_RANGE] = [ring_color] * _KEY_PIXELS
        self.pixels.show()

    def _animate_stop(self):
        if getattr(self, '_animate_thread', None):
            self._animate_thread.stop()
        self._animate_thread = None

    def _animate_start(self):
        if self._animate_thread is None:
            self._animate_thread = AnimateThread(self.pixels, self.ring_brightness, self.delay)
            self._animate_thread.start()

    def pulseButton(self, color=Color.WHITE, duration=1) -> None:
        self._animate_start()
        self._animate_thread.button_animation = {
            "type": AnimationType.PULSE,
            "color": color,
            "duration": duration
        }

    def flashButton(self, color=Color.WHITE, duration=1):
        self._animate_start()
        self._animate_thread.button_animation = {
            "type": AnimationType.FLASH,
            "color": color, "duration": duration
        }

    def stopButton(self):
        if self._animate_thread is not None:
            if (
                self._animate_thread.ring_animation is None
                and
                self._animate_thread.key1_animation is None
                and
                self._animate_thread.key2_animation is None
            ):
                self._animate_stop()
            else:
                self._animate_thread.button_animation = None
        self.pixels[_BUTTON_RANGE] = [Color.OFF] * _BUTTON_PIXELS
        self.pixels.show()

    def unicornRing(self, duration=25) -> None:
        self._animate_start()
        self._animate_thread.ring_animation = {
            "type": AnimationType.UNICORN,
            "color": Color.OFF,
            "duration": duration
        }

    def pulseRing(self, color=(0, 0, 100), duration=2.5) -> None:
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.ring_animation = {
            "type": AnimationType.PULSE,
            "color": ring_color,
            "duration": duration
        }

    def chaseRing(self, color=(0, 0, 255), duration=5) -> None:
        self._animate_start()
        self._animate_thread.ring_animation = {
            "type": AnimationType.CHASE,
            "color": color,
            "duration": duration
        }

    def flashRing(self, color=(0, 0, 100), duration=2.5):
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.ring_animation = {
            "type": AnimationType.FLASH,
            "color": ring_color,
            "duration": duration
        }

    def stopRing(self) -> None:
        if self._animate_thread is not None:
            if (
                self._animate_thread.button_animation is None
                and
                self._animate_thread.key1_animation is None
                and
                self._animate_thread.key2_animation is None
            ):
                self._animate_stop()
            else:
                self._animate_thread.ring_animation = None
        self.pixels[_RING_RANGE] = [Color.OFF] * _RING_PIXELS
        self.pixels.show()

    def stopKey1(self) -> None:
        if self._animate_thread is not None:
            if (
                self._animate_thread.button_animation is None
                and
                self._animate_thread.ring_animation is None
                and
                self._animate_thread.key2_animation is None
            ):
                self._animate_stop()
            else:
                self._animate_thread.key1_animation = None
        self.pixels[_KEY1_RANGE] = [Color.OFF] * _KEY_PIXELS
        self.pixels.show()

    def stopKey2(self) -> None:
        if self._animate_thread is not None:
            if (
                self._animate_thread.button_animation is None
                and
                self._animate_thread.ring_animation is None
                and
                self._animate_thread.key1_animation is None
            ):
                self._animate_stop()
            else:
                self._animate_thread.key2_animation = None
        self.pixels[_KEY2_RANGE] = [Color.OFF] * _KEY_PIXELS
        self.pixels.show()

    def chaseKey1(self, color=(0, 0, 255), duration=5) -> None:
        self._animate_start()
        self._animate_thread.key1_animation = {
            "type": AnimationType.CHASE,
            "color": color,
            "duration": duration
        }

    def chaseKey2(self, color=(0, 0, 255), duration=5) -> None:
        self._animate_start()
        self._animate_thread.key2_animation = {
            "type": AnimationType.CHASE,
            "color": color,
            "duration": duration
        }

    def flashKey1(self, color=(0, 0, 100), duration=2.5):
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.key1_animation = {
            "type": AnimationType.FLASH,
            "color": ring_color,
            "duration": duration
        }

    def flashKey2(self, color=(0, 0, 100), duration=2.5):
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.key2_animation = {
            "type": AnimationType.FLASH,
            "color": ring_color,
            "duration": duration
        }

    def pulseKey1(self, color=Color.WHITE, duration=1) -> None:
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.key1_animation = {
            "type": AnimationType.PULSE,
            "color": ring_color,
            "duration": duration
        }

    def pulseKey2(self, color=Color.WHITE, duration=1) -> None:
        self._animate_start()
        ring_color = tuple(int(c * self.ring_brightness) for c in color)
        self._animate_thread.key2_animation = {
            "type": AnimationType.PULSE,
            "color": ring_color,
            "duration": duration
        }


class AnimateThread(threading.Thread):
    def __init__(self, pixels, ring_brightness, delay):
        super(AnimateThread, self).__init__()
        self.daemon = True
        self.stoprequest = threading.Event()
        self.pixels = pixels
        self.delay = delay
        self.ring_brightness = ring_brightness
        self._button_animation = None
        self._ring_animation = None
        self._key1_animation = None
        self._key2_animation = None
        self._button_frame = 0
        self._ring_frame = 0
        self._key1_frame = 0
        self._key2_frame = 0

    @property
    def button_animation(self):
        return self._button_animation

    @button_animation.setter
    def button_animation(self, value):
        self._button_animation = value
        self._button_frame = 0

    @property
    def ring_animation(self):
        return self._ring_animation

    @ring_animation.setter
    def ring_animation(self, value):
        self._ring_animation = value
        self._ring_frame = 0

    @property
    def key1_animation(self):
        return self._key1_animation

    @key1_animation.setter
    def key1_animation(self, value):
        self._key1_animation = value
        self._key1_frame = 0

    @property
    def key2_animation(self):
        return self._key2_animation

    @key2_animation.setter
    def key2_animation(self, value):
        self._key2_animation = value
        self._key2_frame = 0

    def start(self):
        self.stoprequest.clear()
        super(AnimateThread, self).start()

    def stop(self, timeout=10):
        self.stoprequest.set()
        self.join(timeout)
        self.button_animation = None
        self.ring_animation = None
        self.key1_animation = None
        self.key2_animation = None

    def join(self, timeout=None):
        super(AnimateThread, self).join(timeout)
        if self.is_alive():
            assert timeout is not None
            raise RuntimeError(
                "Thread failed to die within %d seconds" % timeout)

    def run(self):
        while True:
            # Note that the animate functions control iterating and resetting their own frames
            # Get a frame for the ring
            ring_pixels = self._animate_ring(self.pixels[_RING_RANGE])
            self.pixels[_RING_RANGE] = ring_pixels
            # Get a frame for the button
            button_pixels = self._animate_button(self.pixels[_BUTTON_RANGE])
            self.pixels[_BUTTON_RANGE] = button_pixels
            # Get a frame for key1
            key1_pixels = self._animate_key1(self.pixels[_KEY1_RANGE])
            self.pixels[_KEY1_RANGE] = key1_pixels
            # Get a frame for key2
            key2_pixels = self._animate_key2(self.pixels[_KEY2_RANGE])
            self.pixels[_KEY2_RANGE] = key2_pixels
            # Show them at the same time
            self.pixels.show()
            # Wait a bit then get the next frame
            if self.stoprequest.wait(self.delay):
                break

    def _animate_button(self, pixels):
        if self.button_animation is None:
            return [self.pixels[_BUTTON_START]] * len(pixels)

        (self._button_frame, pixels) = self._animate(
            num_pixels=len(pixels),
            animation_type=self.button_animation["type"],
            frame=self._button_frame,
            color=self.button_animation["color"],
            duration=self.button_animation["duration"])

        return pixels

    def _animate_ring(self, pixels):
        if self.ring_animation is None:
            return [self.pixels[_RING_START]] * len(pixels)

        (self._ring_frame, pixels) = self._animate(
            num_pixels=len(pixels),
            animation_type=self.ring_animation["type"],
            frame=self._ring_frame,
            color=self.ring_animation["color"],
            duration=self.ring_animation["duration"])

        return pixels

    def _animate_key1(self, pixels):
        if self.key1_animation is None:
            return [self.pixels[_KEY1_START]] * len(pixels)

        (self._key1_frame, pixels) = self._animate(
            num_pixels=len(pixels),
            animation_type=self.key1_animation["type"],
            frame=self._key1_frame,
            color=self.key1_animation["color"],
            duration=self.key1_animation["duration"])

        return pixels

    def _animate_key2(self, pixels):
        if self.key2_animation is None:
            return [self.pixels[_KEY2_START]] * len(pixels)

        (self._key2_frame, pixels) = self._animate(
            num_pixels=len(pixels),
            animation_type=self.key2_animation["type"],
            frame=self._key2_frame,
            color=self.key2_animation["color"],
            duration=self.key2_animation["duration"])

        return pixels

    def wheel(self, pos):
        # Taken from the Adafruit Neopixel example code.
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)

        # As this is used for the ring, turn down the brightness
        r = int(r * self.ring_brightness)
        g = int(g * self.ring_brightness)
        b = int(b * self.ring_brightness)

        return (r, g, b)

    def _flash(self, num_pixels, frame, color, duration):
        framesOn = (duration / self.delay)
        if frame <= framesOn:
            pixels = [color] * num_pixels
            frame += 1
        else:
            pixels = [Color.OFF] * num_pixels
            frame += 1

        # Max length of animation is twice the length of the duration
        if frame > framesOn * 2:
            frame = 0
        return (frame, pixels)

    def _pulse(self, num_pixels, frame, color, duration):
        brightness = frame * (2.5 * self.delay / duration)
        if brightness > 1.25:
            brightness = 2.5 - brightness
        if brightness > 1:
            brightness = 1
        elif brightness < 0.1:
            # RGB lights a bit too flikery below 10%
            brightness = 0
        # We now have brightness as a percentage (0-1), apply equally to RGB channels
        color = tuple(int(c * brightness) for c in color)
        pixels = [color] * num_pixels
        frame += 1
        # Max length of animation is the duration
        if frame > (duration / self.delay):
            frame = 0
        return (frame, pixels)

    def _unicorn(self, num_pixels, frame, duration):
        pixels = [Color.OFF] * num_pixels
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + frame
            pixels[i] = self.wheel(pixel_index & 255)
        frame += 1 + int(25 / duration)
        # Max length of animation is 255
        if frame > 255:
            frame = 0
        return (frame, pixels)

    def _chase(self, num_pixels, frame, color):
        # Define the brightness sequence for pattern
        min_brightness = self.ring_brightness / 50
        # Add a leading brighter pixel
        pattern = [self.ring_brightness - ((self.ring_brightness - min_brightness) / 10)]
        # Have a bunch of full brightness pixels
        pattern += ([self.ring_brightness] * int(num_pixels / 6))
        for i in range(int(num_pixels / 3)):
            # linear drop in brightness to min brightness
            pattern.append(
                self.ring_brightness
                - (((self.ring_brightness - min_brightness) / int(num_pixels / 3)) * i)
            )
        # rest of the pixels at min brightness
        pattern += [min_brightness] * (num_pixels - len(pattern))

        # Apply brightness to pixels & reverse the order
        pixels = []
        for pb in reversed(pattern):
            pixel = tuple(int(c * pb) for c in color)
            pixels.append(pixel)

        # Rotate the pixels clockwise
        pixels = (pixels[-frame:] + pixels[:-frame])
        frame += 1
        if frame >= num_pixels:
            frame = 0

        return (frame, pixels)

    def _animate(self, num_pixels, animation_type, frame, color, duration):

        if animation_type == AnimationType.FLASH:
            return self._flash(num_pixels, frame, color, duration)

        elif animation_type == AnimationType.PULSE:
            return self._pulse(num_pixels, frame, color, duration)

        elif animation_type == AnimationType.UNICORN:
            return self._unicorn(num_pixels, frame, duration)

        elif animation_type == AnimationType.CHASE:
            return self._chase(num_pixels, frame, color)
