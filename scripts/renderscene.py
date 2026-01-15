from PIL import Image
import numpy as np
from ledmatrix.sources.imagesource import ImageSource
from ledmatrix.renderer import Renderer
from ledmatrix.displaycontroller import DisplayController



img_path = "../assets/Mario.jpg"
img_src = ImageSource(128,64, (0,-1), 1)
display = DisplayController()
renderer = Renderer(display)
img_src.upload(img_path)
renderer.compositor.add_layer(img_src)
renderer.start()







