from LEDMatrix.matrix import LEDMatrix
from LEDMatrix.config import WIDTH, HEIGHT
import numpy as np

class Compositor:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.framebuffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.matrix = LEDMatrix()
        self.layers = []

    def add_layer(self, source):
        self.layers.append(source)

    def remove_layer(self, source):
        self.layers.remove(source)

    def clear_layers(self):
        for layer in self.layers:
            self.remove_layer(layer)

    def format_to_buffer(self, source) -> np.ndarray:
        layer = self.align_to_buffer_format(source)
        layer = self.fit_data_to_buffer(layer)
        layer = self.clamp_color_data(layer)
        return layer

    def render_buffer(self):
        self.framebuffer.fill(0)
        for layer in self.layers:
            layerBuffer = layer.render()
            l
        self.framebuffer = self.format_to_buffer(self.framebuffer)
        self.matrix.display_framebuffer(self.framebuffer)


    def align_to_buffer_format(self, source) -> np.ndarray:
        if isinstance(source, np.ndarray):
            arr = source
        elif isinstance(source, Image.Image):
            arr = np.asarray(source.convert("RGB"))
        elif hasattr(source, "to_numpy"):
            arr = source.to_numpy()
        else:
            raise TypeError("Unsupported frame source: {type(source)}")
        if arr.ndim == 2:
            arr = np.stack([arr]*3, axis=-1)
        if arr.shape[-1] != 3:
            raise ValueError("Expected RGB data")
        return arr

    def fit_data_to_buffer(self, arr: np.ndarray) -> np.ndarray:
        h, w, _ = arr.shape
        out = np.zeros(self.height, self.width, 3), dtype=arr.dtype

        copy_w = min(w, self.width)
        copy_h = min(h, self.height)
        out[:copy_h,:copy_w] = arr[:copy_h,:copy_w, :]
        return out

    def clamp_color_data(self, arr: np.ndarray) -> np.ndarray:
        if arr.dtype != np.uint8:
            arr = np.clip(arr, 0, 255).astype(np.uint8)
        return arr

