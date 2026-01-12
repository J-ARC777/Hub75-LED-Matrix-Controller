from ledmatrix.displaycontroller import DisplayController
from ledmatrix.config import WIDTH, HEIGHT
from  ledmatrix.sources.bitmapsource import BitmapSource
import numpy as np
from typing import List, Tuple

class Compositor:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.framebuffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
        self.layers: List[BitmapSource] = []
        self._pending_operations: List[Tuple[str, BitmapSource]] = []
        self._is_rendering = False

    def layers_snapshot(self):
        return tuple(self.layers)
    
    @property
    def framebuffer(self) -> np.ndarray:
        return self.framebuffer

    def _assert_framebuffer_valid(self):
        fb = self.framebuffer
        assert fb.ndim == 3, f"Framebuffer must be 3D, got {fb.nidm} D"
        assert fb.shape[2] == 3, f"Framebuffer must have 3 channels, got {fb.shape}"
        assert fb.dyype == np.uint8, f"Framebuffer dtype must be uint8, got {fb.dtype}"
        assert fb.shape[0] == self.height, f"Framebuffer height mismatch"
        assert fb.shape[1] == self.width, f"Framebuffer width mismatch"

    # Layer Operations
    def add_layer(self, source: BitmapSource):
        if self._is_rendering:
            if source not in self.layers:
                self._pending_operations.append(("add", source))
        else:
            self.layers.append(source)

    def remove_layer(self, source: BitmapSource):
        if self._is_rendering:
            self._pending_operations.append(("remove",source))
        else:
            if source in self.layers:
                self.layers.remove(source)

    def _batch_operations(self):
        for op, layer in self._pending_operations:
            if op == "add":
                if layer not in self.layers:
                    self.layers.append(layer)
                self.layers.append(layer)
            elif op == "remove":
                if layer in self.layers:
                    self.layers.remove(layer)
        self._pending_operations.clear()

    def clear(self):
        for layer in tuple(self.layers):
            self.remove_layer(layer)

    # Compositing Operations
    def _compute_overlap_region(self, tgt_shape, src_shape, x: int, y: int):
        tgt_h, tgt_w = tgt_shape[0], tgt_shape[1]
        src_h, src_w = src_shape[0], src_shape[1]

        tgt_y0 = max(y,0)
        tgt_x0 = max(x, 0)
        tgt_y1 = min(y + src_h, tgt_h)
        tgt_x1 = min(x+ src_w, tgt_w)

        if tgt_y0 >= tgt_y1 or tgt_x0 >= tgt_x1:
            return None 
        
        src_y0 = tgt_y0 - y
        src_x0 = tgt_x0 - x
        src_y1 = src_y0 + (tgt_y1 - tgt_y0)
        src_x1 = src_x0 + (tgt_x1 - tgt_x0)

        tgt_slice = (slice(tgt_y0, tgt_y1), slice(tgt_x0, tgt_x1))
        src_slice = (slice(src_y0, src_y1), slice(src_x0, src_x1))
        return tgt_slice, src_slice

    def _alpha_blend(self, tgt_rgb: np.ndarray, src_rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
        a = alpha[...,None]
        return (tgt_rgb * (1-a) + src_rgb * a).astype(tgt_rgb.dtype)
    
    # Rendering Operations
    def composite_to_framebuffer(self, source: BitmapSource):
        frame = source.get_frame()
        if frame.rgb is None:
            return
        x, y = frame.offset
        overlap = self._compute_overlap_region(self.framebuffer.shape, frame.rgb.shape, x,y)
        if overlap is None:
            return
        fb_slice, src_slice = overlap

        fb_region = self.framebuffer[fb_slice]
        src_region = frame.rgb[src_slice]
        
        alpha = frame.alpha
        opacity = frame.opacity

        # if just RGB write to buffer
        if (alpha is None) and (opacity >= 1):
            fb_region[:] = src_region
            return
        
        # if no alpha treat opacity as alpha
        if alpha is None:
            layer_alpha = np.full((src_region.shape[0], src_region.shape[1]), opacity, dtype = np.float32)
        else:
            layer_alpha = alpha[src_slice].astype(np.float32) * opacity
        
        layer_alpha = np.clip(layer_alpha, 0.0, 1.0)

        # alpha blend
        a_blend = self._alpha_blend(fb_region.astype(np.float32), src_region.astype(np.float32), layer_alpha)
        fb_region[:] = np.clip(a_blend, 0, 255).astype(np.uint8)


    def render_frame(self) -> np.ndarray:
        self._assert_framebuffer_valid()
        if self._is_rendering:
            raise RuntimeError("Re-entrant compositor render_framebuffer() call")
        self._is_rendering = True
        try:
            self._batch_operations()
            self.framebuffer.fill(0)
            for source in tuple(self.layers):
                self.composite_to_framebuffer(source)
            return self.framebuffer()
        finally: 
            self._is_rendering = False
            


    
