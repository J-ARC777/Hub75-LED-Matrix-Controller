from PIL import Image
import numpy as np
from Sources.ImageSource import ImageSource
from compositor import Compositor



img_path = "../assets/Mario.jpg"
img_buffer = ImageSource(128,64)

comp = Compositor()
img_buffer.write(img_path)
comp.add_layer(img_buffer)
comp.render_framebuffer()







