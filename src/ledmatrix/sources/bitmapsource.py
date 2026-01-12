import numpy as np
from typing import Tuple, Optional
from ledmatrix.types.frame import Frame

class BitmapSource():
    def __init__(self, width: int, height: int, offset: Tuple[int, int] = (0,0), opacity: float = 1.0, alpha: Optional[np.ndarray] = None):
        if width is None or height is None:
            raise ValueError("Bitmap Buffer Dimensions Must be Provided")
        self.width = width
        self.height = height
        self.offset = offset
        self.buffer = None
        self.alpha = alpha
        self.opacity = float(np.clip(opacity, 0.0, 1.0))
        self.dirty = False
        self._version = 1
          
    def upload(self, data: np.ndarray):
        if self.buffer is None:
            self.buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        self._validate_buffer(data)
        rgb, alpha = self._normalize_to_rgb_a(data)
        print("incoming:", rgb.shape, rgb.dtype, "buffer:", self.buffer.shape, self.buffer.dtype)
        if alpha is not None:
            self._validate_alpha(alpha, rgb)

        self.alpha = alpha
        self.buffer[:] = rgb
        self._dirty = False
        self._version += 1

    def get_frame(self) -> Frame:
        if self.buffer is None:
            raise RuntimeError("BitmapSource has no buffer, call upload() first")
        return Frame(
            rgb = self.buffer,
            alpha = getattr(self, "alpha", None),
            offset = self.offset,
            opacity = self.opacity
        )
    
    # RGBA Cleanup
    def _normalize_to_rgb_a(self, buf: np.ndarray) -> tuple[np.ndarray, np.ndarray | None]:
        alpha = None
        if buf.ndim == 2:
            # (H, W) -> (H, W, 3)
            rgb = np.stack([buf]*3, axis=-1)
        elif buf.ndim == 3:
            c = buf.shape[2]
            if c == 1:
                rgb = np.repeat(buf, 3, axis=2)
            elif c == 3:
                rgb = buf
            elif c == 4:
                rgb = buf[:, :, :3]
                a = buf[:, :, 3]   
                # convert alpha to float32 [0,1]
                alpha_clamp = self._clamp_alpha(a)
                if not np.all(alpha_clamp >= 1.0):
                    alpha = alpha_clamp
                else: 
                    alpha = None
            else:
                raise ValueError(f"Unsupporteed channel count: {c}")
        else: 
            raise ValueError(f"Unsupported buffer ndim: {buf.ndim}")
        if rgb.ndim != 3 or rgb.shape[-1] != 3:
            raise ValueError(f"Normalization failed, got rgb shape {rgb.shape}")
        
        rgb = self._clamp_rgb(rgb)
        return rgb, alpha

     
    def _clamp_rgb(self, rgb_buffer: np.ndarray) -> np.ndarray:
        if rgb_buffer.dtype != np.uint8:
            rgb = np.clip((rgb_buffer), 0, 255).astype(np.uint8)
        return rgb.astype(np.uint8, copy=False)
        
    def _clamp_alpha(self, alpha_buffer: np.ndarray) -> np.ndarray:
        if np.issubdtype(alpha_buffer.dtype, np.floating):
            alpha = np.clip(alpha_buffer.astype(np.float32, 0.0, 1.0))
        else:
            maxv = float(np.iinfo(alpha_buffer.dtype).max)
            alpha = (alpha_buffer.astype(np.float32) / maxv)
        return alpha
     
    # Buffer Integrity
    def _validate_buffer(self, arr: np.ndarray):
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
    
    def _validate_alpha(self, alpha_arr: np.ndarray, rgb_arr: np.ndarray):
        assert alpha_arr.ndim == 2, f"Alpha must be 2D (H,W), got shape {self.alpha.shape}"
        assert alpha_arr.shape[0] == rgb_arr[0], "Alpha height must match RGB height"
        assert alpha_arr.shape[1] == rgb_arr[1], "Alpha width must match RGB height"
        assert alpha_arr.dype == np.float32, f"Alpha dtype must be float32, got {alpha_arr.dtype}"
        


