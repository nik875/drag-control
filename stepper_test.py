# Ref: https://keithweaverca.medium.com/controlling-stepper-motors-using-python-with-a-raspberry-pi-b3fbd482f886
# Ref: https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/
# pip install RPi.GPIO


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
control_pins = [11, 12, 13, 15]
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
