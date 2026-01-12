from PIL import Image
import numpy as np
from Sources.imagesource import ImageSource
from renderer import Renderer
from displaycontroller import DisplayController



img_path = "../assets/Mario.jpg"
img_src = ImageSource(128,64)
display = DisplayController()
renderer = Renderer(display)
img_src.upload(img_path)
renderer.compositor.add_layer(img_src)
renderer.start()







