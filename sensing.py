import time
import copy
from collections import deque
import numpy as np
from scipy import stats
import imu.simpleimu as imu
import altimeter.altimeter as alt
from logger import Logger


READS_PER_SECOND = 370  # emperically determined


class SensorMgr:
    def __init__(self, buffer_size=READS_PER_SECOND // 10, alpha=.001,
            delta=imu.gravity_fps / 2, log_interval=.1):
        self.alpha = alpha
        self.delta = delta
        self.state = 'ground'
        self.data = deque(imu.sample(buffer_size))
        self.last_measurement = time.time()
        self.velocity = 0
        self.baseline = np.mean(self.data)
        self.data = deque(map((lambda i: i - self.baseline), self.data))
        self.initial_altitude = alt.sample_time(.1)
        self.current_altitude = self.initial_altitude
        self.logger = Logger('mission_log.csv')
        self.logger.log_data(self.generate_report())
        self.last_log_time = time.time()
        self.log_interval = log_interval

    def record_data(self):
        # Run in loop to record new data
        self.data.popleft()
        self.data.append(imu.read_net_acc() - self.baseline)
        delta = self.data[-1] * (time.time() - self.last_measurement)
        self.last_measurement = time.time()
        if self.state != 'ground':
            self.velocity += (delta if self.state == 'engine_burn' else -delta)
        else:
            self.velocity = 0
        self.current_altitude = alt.sample_time(.01)
        if time.time() > self.last_log_time + self.log_interval:
            self.logger.log_data(self.generate_report())
            self.last_log_time = time.time()

    def generate_report(self):
        return [time.time(), self.state, np.mean(self.data), self.velocity,
                self.current_altitude]

    def detect_change(self):
        # take the current data as a baseline and wait for a significant change
        current_baseline = np.mean(self.data)
        self.data = deque(map((lambda i: i - self.baseline),
            imu.sample(len(self.data))))
        while stats.ttest_1samp(self.data, current_baseline)[1] > self.alpha \
                or abs(np.mean(self.data) - current_baseline) < self.delta:
            self.record_data()

    def wait_for_launch(self):
        assert self.state == 'ground'
        # wait in loop until launch is detected
        self.detect_change()  # Assume launch is the only change possible
        self.state = 'engine_burn'

    def wait_for_meco(self):
        assert self.state == 'engine_burn'
        # wait in loop until main engine cutoff detected
        while np.mean(self.data) >= self.baseline or \
                stats.ttest_1samp(self.data, self.baseline)[1] >= self.alpha:
            self.record_data()
        self.state = 'ascent'

    def detect_inflection(self):
        # wait in loop until altitude starts falling
        self.state = 'descent'

    def detect_landing(self):
        # wait in loop until we land
        pass


if __name__ == '__main__':
    mgr = SensorMgr()
    mgr.wait_for_launch()
    print('Launch detected')
    mgr.wait_for_meco()
    print('MECO detected')

