from ledmatrix.matrix import LEDMatrix
import numpy as np

class DisplayController:
    _active_instance = None
    def __init__(self, brightness: float = 1.0, pwm_bits: int = 8):
        if Display._active_instance is not None:
            raise RuntimeError("Only one DisplayController may exist at a time")
        
        self._matrix = LEDMatrix()
        self.brightness = brightness
        self.pwm_bits = pwm_bits

    def set_brightness(self, value: float):
        value = max(0.0, min(1.0), value)
        self.matrix.set_brightness(value)

    def set_pwm_bits(self, value: int):
        self.matrix.set_pwm_bits(value)
    
    def present(self, fb: np.ndarray):
        self._assert_frame_valid(fb)
        self.set_brightness(self.brightness)
        self.matrix.framebuffer[:] = fb
        self.matrix.display()

    def shutdown(self):
        DisplayController._active_instance = None
        self._matrix = None

    def _assert_frame_valid(self, frame: np.ndarray):
        fb = self.matrix.framebuffer
        if frame.shape != fb.shape:
            raise ValueError(f"Frame shape {frame.shape} does not match matrix {fb.shape}")
        if frame.dtype != fb.dtype:
            raise TypeError(f"Frame dtype {frame.dtype} does not match matrix {fb.dtype}")
        if frame.ndim != 3 or frame.shape[2] != 3:
            raise ValueError("Expected (H, W, 3) RGB frame")

    @classmethod
    def active(cls):
        return cls._active_instance