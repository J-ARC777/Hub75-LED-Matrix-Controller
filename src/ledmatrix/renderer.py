import time
from typing import Optional, Callable, List, Protocol

from ledmatrix.compositor import Compositor
from ledmatrix.displaycontroller import DisplayController
from ledmatrix.sources.bitmapsource import BitmapSource

class Updatable(Protocol):
    def update(self, dt:float) -> None: ...


class UpdateManager:
    def __init__(self):
        self._items = List[Updatable] = []
    
    def add(self, item: Updatable):
        self._items.append(item)

    def __call__(self, dt:float):
        for item in self._items:
            item.update(dt)

class Renderer: 
    def __init__(self, display_output: DisplayController, target_fps: int = 60, fixed_hz: int = 60):
        
        self.target_fps = target_fps
        if not isinstance(display_output, DisplayController):
            raise TypeError("Valid DisplayController must be provided")
        self.display = display_output
        self.compositor = Compositor()
        self.update_manager = UpdateManager()

        self.fixed_dt = 1.0 / fixed_hz
        self._frame_dt = 1.0 / target_fps
        self._active = False

        # optional external hook for time based logic
        # signature updated(dt: float) -> None
        self.update_hook: Optional[Callable[[float], None]] = self.update_manager

    def register_updatable(self, item: Updatable):
        self.update_manager.add(item)

    def add_source(self, source: BitmapSource):
        self.compositor.add_layer(source)
        
    def start(self):
        self._active = True
        self._render()

    def stop(self):
        self._active = False

    def _render(self):
        previous_frame = time.perf_counter()
        accumulator = 0.0
        while self._active:
            current_time = time.perf_counter()
            dt = current_time - previous_frame
            previous_frame = current_time

            dt = min(dt, 0.25)
            accumulator += dt
            
            while accumulator >= self.fixed_dt: 
                if self.update_hook is not None:
                    self.update_hook(self.fixed_dt)
                accumulator -= self.fixed_dt
            frame = self.compositor.render_frame()
            self.display.present(frame)

            elapsed = time.perf_counter() - current_time
            sleep_time = self._frame_dt - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)



