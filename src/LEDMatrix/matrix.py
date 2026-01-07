import numpy as np
from PIL import Image

import adafruit_blinka_raspberry_pi5_piomatter as piomatter
from .config import WIDTH, HEIGHT, ADDR_LINES, PINOUT, COLORSPACE

class LEDMatrix:
    def __init__(self):
        self.width = WIDTH
	self.height = HEIGHT
	self.geometry = piometter.Geometry( width = self.width,
				            height = self.height,
				            n_addr_lines = ADDR_LINES,
					    rotation=piomatter.orientation.normal
	)
        self._framebuffer = np.zeros( (self.height, self.width, 3) dtype=np.uint8)
	self._matrix = piometter.PioMatter( colorspace = COLORSPACE,
                                            pinout = PINOUT,
                                            framebuffer = self.framebuffer,
                                            geometry = self.geometry
        )



def display(self):
	self._matrix.show()

def clear(self):
	self.framebuffer.fill(0)
	self.render_framebuffer()
