from LEDMatrix.matrix import LEDMatrix
from LEDMatrix.config import WIDTH, HEIGHT
from LEDMatrix.Sources.BitmapSource import BitmapSource
import numpy as np

class Compositor:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.framebuffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.matrix = LEDMatrix()
        self.layers: list[BitmapSource] = []


    def add_layer(self, source: BitmapSource):
        self.layers.append(source)

    def remove_layer(self, source: BitmapSource):
        self.layers.remove(source)

    def clear_layers(self):
        for layer in self.layers:
            self.remove_layer(layer)

    def merge_source(self, source: BitmapSource):
        src = source.buffer
        h,w,_ = src.shape
        fb = self.framebuffer
        
        src_x = source.offset[0]
        src_y = source.offset[1]
        fb_x0 = max(src_x, 0)
        fb_y0 = max(src_y, 0)

        fb_x1 = min(fb_x0 + w, fb.shape[1])
        fb_y1 = min(fb_y0 + h, fb.shape[0])

        if fb_y0 >= fb_y1 or fb_x0 >= fb_x1:
            return #offscreen
        
        src_y0 = fb_y0 - src_y
        src_x0 = fb_x0 - src_x
        src_y1 = src_y0 + (fb_y1 - fb_y0)
        src_x1 = src_x0 + (fb_x1 - fb_x0)

        fb[fb_y0:fb_y1, fb_x0:fb_x1] = src[src_y0:src_y1, src_x0:src_x1] 


    def alpha_blend(tgt: np.ndarray, src: np.ndarray, alpha: np.ndarray):
        a = alpha[...,None]
        return (src * (1-a) + src * a).astype(tgt.dtype)
    
    def composite_to_framebuffer(self, source: BitmapSource):
        self.merge_source(source)

    def render_framebuffer(self):
        self.framebuffer.fill(0)
        for source in self.layers:
            self.composite_to_framebuffer(source)
        self.matrix.display_framebuffer(self.framebuffer)

    
