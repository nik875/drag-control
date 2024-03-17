#!/usr/bin/python
#
#       This is the base code needed to get usable angles from a BerryIMU
#       using a Complementary filter. The readings can be improved by
#       adding more filters, E.g Kalman, Low pass, median filter, etc..
#       See berryIMU.py for more advanced code.
#
#       The BerryIMUv1, BerryIMUv2 and BerryIMUv3 are supported
#
#       This script is python 2.7 and 3 compatible
#
#       Feel free to do whatever you like with this code.
#       Distributed as-is; no warranty is given.
#
#       https://ozzmaker.com/berryimu/


import time
from . import IMU


IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass
gravity_fps = 32.17405


def read_data():
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    acc = [ACCx, ACCy, ACCz]

    acc_in_gs = [i * .244 / 1000 for i in acc]
    return [i * gravity_fps for i in acc_in_gs]


def read_net_acc():
    data = read_data()
    xy = (data[0] ** 2 + data[1] ** 2) ** .5
    xyz = (xy ** 2 + data[2] ** 2) ** .5
    return xyz


def sample(size):
    return [read_net_acc() for _ in range(size)]


def sample_time(duration):
    st = time.time()
    data = []
    while time.time() < st + duration:
        data.append(read_net_acc())
    return data


if __name__ == '__main__':
    results = sample_time(5)
    print(len(results), sum(results) / len(results))
