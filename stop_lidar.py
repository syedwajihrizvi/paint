"""
Consume LIDAR measurement file and create an image for display.
Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!
Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.
"""
from util import movingAverage
import os
from math import cos, sin, pi, floor
import pygame
from rplidar import RPLidar
from tracker import Tracker


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

try:
    while True:
        lidar.stop()
        print(lidar.get_health())
except KeyboardInterrupt:
    print('Stoping.')
lidar.disconnect()
