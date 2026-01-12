from PIL import Image
import numpy as np
from typing import Tuple, Union, Optional
from ledmatrix.sources.bitmapsource import BitmapSource


class ImageSource(BitmapSource):
    def __init__(self, width, height, offset: Tuple[int, int] = (0,0), opacity: float = 1.0, alpha: Optional[np.ndarray] = None ):
        if width is None or height is None:
            raise ValueError("Image Buffer Dimensions must be provided if no intial image data is provided")     
        super().__init__(width, height, offset, opacity, alpha)
        self._img: Optional[Image.Image] = None

    def _load_image(self, data: Union[str,Image.Image]) -> Image.Image:
        if isinstance(data, str):
            img = Image.open(data)
            img.load()
            return img
        if isinstance(data, Image.Image):
            return data
        raise TypeError("ImageSource.write() only accepts PIL.Image.Image or file path string")

    def upload(self, data: Union[str, Image.Image], mode:str = "fit"):
        img = self._load_image(data)
        self._img = img

        if mode == "fit":
            img = img.resize((self.height, self.width), Image.LANCZOS)
        elif mode == "cover":
            img = self._cover_img(img)
        else:
            raise ValueError("Unknown Image scaling mode. Options are 'fit', 'cover'")
        rgba = np.asarray(img.convert("RGBA"))
        
        print(type(img), img.size, img.mode)
        print(type(rgba), getattr(rgba, "shape", None), getattr(rgba, "dtype", None))
        if rgba is None:
            raise TypeError("Image Conversion failed. Please check image path or image data")

        super().upload(rgba)
    
    def resize(self, new_size: Tuple[int, int], mode: str = "fit"):
        self.height, self.width = new_size
        self.buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        if self._img is not None: 
            self.upload(self._img, mode=mode)

    def _cover_image(self, img: Image.Image) -> Image.Image:
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
