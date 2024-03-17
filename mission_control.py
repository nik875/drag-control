import time
from sensing import SensorMgr
from servo_driver import Servo
from imu.simpleimu import gravity_fps


def simulated_apogee(mgr):
    return mgr.velocity ** 2 / (2 * gravity_fps)


def main(target_apogee, target_offset=5):
    time.sleep(5)
    ser = Servo()
    mgr = SensorMgr()
    mgr.wait_for_launch()
    mgr.wait_for_meco()
    while simulated_apogee(mgr) > target_apogee + target_offset:
        ser.max()
    ser.min()
    while True:  # Just record data for the rest of the flight
        mgr.record_data()

