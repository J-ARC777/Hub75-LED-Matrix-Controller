import numpy as np
from PIL import Image

import adafruit_blinka_raspberry_pi5_piomatter as piomatter
from .config import WIDTH, HEIGHT, ADDR_LINES, PINOUT, COLORSPACE

class LEDMatrix:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        self.geometry = piomatter.Geometry( width = self.width, 
                                            height = self.height, 
                                            n_addr_lines = ADDR_LINES, 
                                            rotation=piomatter.orientation.normal )
        
        self._framebuffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        self._matrix = piomatter.PioMatter( colorspace = COLORSPACE,
                                            pinout = PINOUT,
                                            framebuffer = self.framebuffer,
                                            geometry = self.geometry )

    def display(self):
        self._matrix.show()
            
    def display_framebuffer(self, framebuffer: np.ndarray):
        self._framebuffer[:] = framebuffer
        self.display()

    def clear(self):
        self._framebuffer.fill(0)
        self.display()
