import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'


from gpiozero import Servo
import time

servo = Servo(23)
while True:
    servo.min()
    time.sleep(5)
    servo.max()
    time.sleep(5)
