from PIL import Image
import numpy as np
from typing import Tuple
from bitmapsource import BitmapSource


class ImageSource(BitmapSource):
    def __init__(self, width, height, offset: Tuple[int, int] = (0,0)):

        if width is None or height is None:
            raise ValueError("Image Buffer Dimensions must be provided if no intial image data is provided")
        
        super().__init__(width, height, offset)
        self._img = None
        if initial_data is not None: 
            self.write(initial_data)

    def _load_image(self, data) -> Image.Image:
        if isinstance(data, str):
            data = Image.open(data)
        elif not isinstance(data, Image.Image):
            raise TypeError("ImageSource.write() only accepts PIL.Image.Image or file path string")
        else: 
            img = data
        return img
    
    def write(self, data, mode:str = "fit"):
        img = self._load_image(data)
        self._img = img
        if mode == "fit":
            img = img.resize((self.width, self.height), Image.LANCZOS)
        elif mode == "cover":
            img = self._cover_img(img)
        else: 
            raise ValueError("Unknown Image scaling mode. Options are 'fit', 'cover'")
        
        super.write(np.array(data))

    def resize(self, new_size: Tuple[int, int], mode: str = "fit"):
        self.width, self.height = new_size
        self.buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        if self._img is not None: 
            self.write(self._img, mode=mode)

    def _cover_image(self, img: Image.Image) -> Image.Image;
        img_ratio = img.width / img.height
        buf_ratio = self.width / self.height

        if img_ratio > buf_ratio:
            new_height = self.height
            new_width = int(new_height / img_ratio)
        else:
            new_width = self.width
            new_height = int(new_width / img_ratio)
        img_resized = img.resize((new_width, new_height,), Image.LANCZOS)

        left = (new_width - self.width) // 2
        top = (new_height - self.height) // 2
        img_cropped = img_resized.crop((left, top, left + self.width, top+self.height))
        return img_cropped
