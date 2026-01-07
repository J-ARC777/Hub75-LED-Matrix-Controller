from LEDMatrix.matrix import LEDMatrix
from LEDMatrix.config import WIDTH, HEIGHT
import numpy as np


class Compositor:
    def __init__(self):
	self.framebuffer = np.zeros((HEIGHT, WIDTH, 3), dtype=p.uint8)
	self.matrix = LEDMatrix()
	self.layers[]

def add_layer(self, source):
	self.layers.append(source)

def remove_layer(self, source):
	self.layers.remove(source)

def render_frame(self):
	self.framewbuffer.fill(0)
	for layer in self.layers:
	
self.matrix.framebuffer[:] = self.framebuffer
self.matrix.display()



