from PIL import Image
import numpy as np
from ledmatrix.sources.imagesource import ImageSource
from ledmatrix.renderer import Renderer
from ledmatrix.displaycontroller import DisplayController
from ledmatrix.motioncontroller import MotionController


img_path = "../assets/dvdlogo.png"
img_src = ImageSource(16,16)
display = DisplayController()

renderer = Renderer(display)
img_src.upload(img_path)
renderer.compositor.add_layer(img_src)

logo_animator = MotionController(img_src)
logo_animator.set_velocity(0.5, 0.5)
logo_animator.set_screen_bounds(128,64,"bounce")

renderer.register_updatable(logo_animator)
renderer.start()







