import numpy as np
from typing import Tuple

class BitmapSource():
    def __init__(self, width: int, height: int, offset: Tuple[int, int] = (0,0)):
        if width is None or height is None:
            raise ValueError("Bitmap Buffer Dimensions Must be Provided")
        self.width = width
        self.height = height
        self.offset = offset
        self.buffer = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.alpha = None #optional
          
    def write(self, data: np.ndarray):
        self.validate_buffer(data)
        tempBuffer = self.normalize_buffer(data)
        tempBuffer = self.clamp_rgb(tempBuffer)
        self.buffer[:] = tempBuffer
        del tempBuffer

    def validate_buffer(self, arr: np.ndarray):
        if not isinstance(arr, np.ndarray):
            raise TypeError("Bitmap Buffer must be a numpy array")
        if arr.ndim not in (2,3): 
            raise ValueError(f"Invalid bitmap buffer dimmensions: {arr.shape}")
        if arr.ndim == 3 and arr.shape[2] not in (1,3,4):
            raise ValueError (f"Incorrect channel count: {arr.shape[2]}")
        if arr.dtype == np.object_:
              raise TypeError("Object dtype buffers are not supported for bitmaps")
        if not np.isfinite(arr).all():
              raise ValueError("Bitmap contains NaN or infinite values")
        
    def normalize_buffer(self, buf: np.ndarray) -> np.ndarray:
        if buf.ndim == 2:
            # (H, W) -> (H, W, 3)
            buf = np.stack([buf]*3, axis=-1)
        elif buf.shape[2] == 1:
            #(H, W, 1) -> (H, W, 3) (basic grayscale Conversion)
            buf = np.repeat(buf, 3, axis = 2)
        elif buf.shape[2] == 4:
            # RGBA -> RGB + A 
            buf = buf[:, :, :3]
            # Read Alpha from Here    
        if buf.shape[2] != 3:
              # if we are here nothing worked
              raise ValueError("Bitmap Normalization failed to produce RGB Buffer")
        if buf.shape[-1] != 3:
            raise ValueError("Expected RGB data")
        return buf
      
    def clamp_rgb(self, colorBuffer: np.ndarray) -> np.ndarray:
        if colorBuffer.dtype != np.uint8:
            colorBuffer = np.clip((colorBuffer), 0, 255).astype(np.uint8)
            return colorBuffer


