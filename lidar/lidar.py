from util import movingAverage
from math import cos, sin, pi, floor
from rplidar import RPLidar
from rplidar import RPLidarException
from tracker import Tracker
import rplidar
import time
import random

SCAN_BYTE = b'\x20'
SCAN_TYPE = 129


class Lidar:

    def __init__(self, portName):
        self.lidar = RPLidar(portName)
        self.tracker = Tracker()
        self.scan_data = [-1]*360
        self.angles = {}
        self.angles_count = 0
        self.x = 180
        self.y = 90
        self.distance_x = 0
        self.distance_y = 0

    def getData(self):
        self.lidar.motor_speed = 1000
        for scan in self.lidar.iter_scans(scan_type="express", max_buf_meas=False, min_len=100):
            try:
                for (_, angle, distance) in scan:
                    self.scan_data[min([359, floor(angle)])] = distance
            except RPLidarException:
                self.lidar.clean_input()

    def clean(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    def get_heading(self):
        return self.tracker.heading

    def get_distance_x(self):
        return self.distance_x

    def get_distance_y(self):
        return self.distance_y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_count(self):
        return self.angles_count

    def get_latest_scan(self):
        return self.scan_data

    def update_tracker_heading(self, x, y):
        self.tracker.updateHeading(x, y)

    def update_x(self, newValue):
        self.x = newValue

    def update_y(self, newValue):
        self.y = newValue

    def update_x_dist(self, newValue):
        self.distance_x = newValue

    def update_y_dist(self, newValue):
        self.distance_y = newValue

    def get_tracker(self):
        return self.tracker
