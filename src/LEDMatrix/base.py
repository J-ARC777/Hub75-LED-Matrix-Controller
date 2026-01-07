from abc import ABC, abstractmethod
import numpy as np

class FrameSource(ABC)
	
	@abstractmethod
	def render_into(self, framebuffer: np.ndarray):
		pass
