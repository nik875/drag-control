import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'


import time
from gpiozero import AngularServo
MIN_ANGLE = -40
MAX_ANGLE = 52


class Servo:
    def __init__(self):
        s = AngularServo(23, min_angle=MIN_ANGLE, max_angle=MAX_ANGLE)

    def set(angle):
        angle = max([angle, 0])
        s.angle = min([angle + MIN_ANGLE, MAX_ANGLE])
        time.sleep(.1)

    def max():
        s.max()

    def min():
        s.min()

