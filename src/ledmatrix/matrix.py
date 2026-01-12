import numpy as np
from PIL import Image

import adafruit_blinka_raspberry_pi5_piomatter as piomatter
from ledmatrix.config import WIDTH, HEIGHT, ADDR_LINES, PINOUT, COLORSPACE, PWM_MAX, PWM_MIN

class LEDMatrix:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        self.geometry = piomatter.Geometry( width = self.width, 
                                            height = self.height, 
                                            n_addr_lines = ADDR_LINES, 
                                            rotation=piomatter.Orientation.Normal )
        
        self._framebuffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        self._matrix = piomatter.PioMatter( colorspace = COLORSPACE,
                                            pinout = PINOUT,
                                            framebuffer = self._framebuffer,
                                            geometry = self.geometry )

    @property
    def framebuffer(self):
        return self._framebuffer
    
    def display(self):
        self._matrix.show()

    def clear(self):
        self._framebuffer.fill(0)
        self.display()

    def set_brightness(self, value: float):
        value = max(0.0, min(1.0, value))
        self._matrix.brightness = value

    def set_pwm_bits(self, bits: int):
        # Typical range: 6-11. Higher = smoother gradients, larger flicker
        bits = max(PWM_MIN, min(PWM_MAX, bits))
        self._matrix.pwm_bits = bits
        self._matrix.reconfigure()
