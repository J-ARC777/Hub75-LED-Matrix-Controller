import adafruit_blinka_raspberry_pi5_piomatter as piomatter

# Geometry
WIDTH = 128
HEIGHT = 64
ADDR_LINES = 5
CHAIN = 2

# Hardware
PINOUT = piomatter.Pinout.AdafruitMatrixBonnet
COLORSPACE =  piomatterColorspace.RGB888Packed
BIT_DEPTH = 6
PWM_MIN = 6
PWM_MAX = 11