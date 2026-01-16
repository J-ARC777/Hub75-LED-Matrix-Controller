
from typing import List, Optional, TypeAlias
from numpy.typing import NDArray
import numpy as np
from ledmatrix.sources.bitmapsource import BitmapSource


# RGBAFrame: TypeAlias = NDArray[np.uint8]
# RGBFrame = NDArray[np.uint8]
# AlphaU8: TypeAlias = NDArray[np.uint8]
# AlphaF32 = NDArray[np.float32]

# class AnimatedSource(BitmapSource):
#     def __init(self, *args, **kwargs,):
#         super().__init__(*args **kwargs)
#         self._cache =  List[RGBAFrame]

#         self._sequence_alpha = Optional[List[RGBAFrame]]

#         self._cache_window_size = 6
#         self_t = 0.0
#         self._needs_render = True
    
#     def upload(self, sequence: List[RGBAFrame]) {
        
#     }
#     def _update_cache
#     def _select_frame_at_index(self, i:int): 

#     def _pull_from_cache():

#     def update(self, dt: float) -> None: 
#         self_t += dt

#     def get_frame(self) -> Frame:
#         if self.buffer is None:
#             self._alloc
#         return super().get_frame()