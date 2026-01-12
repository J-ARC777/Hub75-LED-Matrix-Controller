from dataclasses import dataclass
import numpy as np
from typing import Optional, Tuple

# This dataclass communicates between sources and the compositor
@dataclass(frozen=True)
class Frame:

    rgb: np.ndarray
    alpha: Optional[np.ndarray]
    offset: Tuple[int, int]
    opacity: float
    blend_mode = "normal"
