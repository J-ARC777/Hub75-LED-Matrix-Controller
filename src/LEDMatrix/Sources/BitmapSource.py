import numpy as np
from typing import Tuple
from PIL import Image

class BitmapSource():
	def __init__(self, width: int, height: int, offset: Tuple[int, int] = (0,0)):
		self.width = width
		self.height = height
		self.offset = offset
		self.buffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)
          

	def write_to_source(self, data):
        arrData = self.align_data_to_buffer(data)
        self.buffer[:] = arrData

    def align_data_to_buffer(self, source) -> np.ndarray:
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


class CompositeLayer():
          def __init__(self, alpha: float)
                self.alpha = alpha

