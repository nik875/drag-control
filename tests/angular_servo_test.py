import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'


import time
from gpiozero import AngularServo
s = AngularServo(23, min_angle=-40, max_angle=52)

while True:
    for i in range(-40, 52, 1):
        s.angle = i
        time.sleep(.01)
    s.angle = -40
