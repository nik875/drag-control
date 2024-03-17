import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'


from gpiozero import Servo
from time import sleep

servo = Servo(23)

try:
    while True:
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")
