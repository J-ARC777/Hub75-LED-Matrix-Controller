from dataclasses import dataclass
from typing import Optional, Tuple, Protocol

@dataclass
class Bounds:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class MotionController:
    def __init__(self, target):
        self.target = target
        self._x = float(target.offset[0])
        self._y = float(target.offset[1])
        self._vx = 0.0
        self._vy = 0.0
        self.bounds: Optional[Bounds] = None
        self._mode: str = "none" # "none | bounce | wrap | clamp "

    def set_velocity(self, vx: float, vy: float) -> None:
        self._vx = float(vx)
        self._vy = float(vy)

    def set_screen_bounds(self, screen_w: int, screen_h: int, mode: str = "bounce") -> None:
        if mode not in ("none", "bounce", "wrap", "clamp"):
            raise ValueError(f"Invalid screenwrap mode: {mode}")
        
        x_min = 0.0
        y_min = 0.0
        x_max = float(screen_w - self.target.width)
        y_max = float(screen_h - self.target.hieght)
        self._bounds = Bounds(x_min, y_min, x_max, y_max)

    def update(self, dt: float) -> None:
        if self._vx == 0.0 and self._vy == 0.0:
            return
    
        self._x += self._vx * dt
        self._y += self._vy * dt

        if self._bounds and self._mode != "none":
            self._resolve_bounds()
        if hasattr(self.target, "set_offset"):
            self.target.set_offset(self._x, self._y)
        else:
            self.target.offset = (self._x, self._y)

    def _resolve_bounds(self) -> None:
        b = self.bounds
        assert b is not None

        if self._mode == "clamp":
            self._x = min(max(self._x, b.x_min), b.x_max)
            self._y = min(max(self._y, b.y_min), b.y_max)

            if self._mode == "wrap":
                w = (b.x_max - b.x_min) if (b.x_max > b.x_min) else 1.0
                h = (b.y_max - b.y_min) if (b.y_max > b.y_min) else 1.0
                while self._x < b.x_min: self._x += w
                while self._x > b.x_max: self._x -= w
                while self._y < b.y_min: self._y += h
                while self._y > b.y_max: self._y -= h
                return

        if self._mode == "bounce":
            if self._x < b.x_min:
                self._x = b.x_min + (b.x_min - self._x)
                self._vx *= -1.0
            elif self._x > b.x_max:
                self._x = b.x_max - (self._x - b.x_max)
                self._vx *= -1.0

            if self._y < b.y_min:
                self._y = b.y_min + (b.y_min - self._y)
                self._vy *= -1.0
            elif self._y > b.y_max:
                self._y = b.y_max - (self._y - b.y_max)
                self._vy *= -1.0



class Movable(Protocol):
    width: int
    height: int
    offset: Tuple[int, int]
