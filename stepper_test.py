# Ref: https://keithweaverca.medium.com/controlling-stepper-motors-using-python-with-a-raspberry-pi-b3fbd482f886
# Ref: https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/
# pip install RPi.GPIO


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
step_sleep = .002
step_count = 4096
direction = False
control_pins = [17, 18, 27, 22]
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]


for i in control_pins:
    GPIO.setup(i, GPIO.OUT)


def cleanup():
    for i in control_pins:
        GPIO.output(i, GPIO.LOW)
cleanup()


try:
    for i in range(0, step_count, -1 if direction else 1):
        for idx, val in enumerate(control_pins):
            GPIO.output(val, step_sequence[i % 8][idx])
        time.sleep(step_sleep)
except KeyboardInterrupt:
    cleanup()
    exit(1)
cleanup()
exit(0)
