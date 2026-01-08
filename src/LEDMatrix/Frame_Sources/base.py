from abc import ABC, abstractmethod
import numpy as np

class FrameSource(ABC):
	
	@abstractmethod
	def render(self) -> np.ndarray:
        pass


# TO DO: implement a Layer class for metadata wrapper 

