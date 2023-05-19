import multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import Manager
from robot import Robot
from lidar.lidar import Lidar
from lidar.reading import Reading
from tracker import Tracker
from util import get_perpendicular_distance, distance_btwn_2_points
from point import Point
from math import cos, sin
import numpy as np
from motor import Motor
import RPi.GPIO as GPIO
from line import Line
from path import Path
from dxf import DXF_Editor
from lidar.reading import Reading
import time
from time import sleep

sample_path = [Line(Point(1143, 406.4), Point(2286, 406.4))]

path_lines = sample_path

dxf_file = DXF_Editor('data/Path1.dxf')
lines = dxf_file.set_lines('data/lines.txt')

robot_path = Path(lines)
robot_path.go()
path_lines = robot_path.get_path()
print(path_lines)
for l in path_lines:
    start = l.start
    end = l.end
    print(f"P1: ({start.x}, {start.y}, {start.is_start}, {start.covered}), P2: ({end.x}, {end.y}, {end.is_start}, {end.covered})")


def sensor(sensor):
    sensor.getData()


def robot_fb(conn):
    robot = Robot(robot_path)
    robot._move_all_motors()
    while True:
        sensor_data = conn.recv()
        robot.controller(sensor_data)


def filter_data(sensor):
    while True:
        latest_data = sensor.get_latest_scan()
        new_reading = process_data(sensor.get_tracker(), latest_data, sensor)
        x = new_reading.x_angle
        y = new_reading.y_angle
        heading = new_reading.heading
        distance_x = new_reading.x_dist
        distance_y = new_reading.y_dist
        sensor.update_x(x)
        sensor.update_y(y)
        sensor.update_x_dist(distance_x)
        sensor.update_y_dist(distance_y)


def handleSensorData(conn, lidar):
    time.sleep(5)
    reading_count = 0
    readings = []
    tracker = lidar.get_tracker()
    prevReading = [lidar.get_x(), lidar.get_y(),
                   lidar.get_heading(), lidar.get_distance_x(), lidar.get_distance_y()]
    sumReadings = [0, 0, 0, 0]

    while True:
        x = lidar.get_x()
        y = lidar.get_y()
        heading = lidar.get_heading()
        distance_x = lidar.get_distance_x()
        distance_y = lidar.get_distance_y()
        if (distance_btwn_2_points(distance_x, distance_y, prevReading[3], prevReading[4])) < 700:
            reading = Reading(x, y, heading, distance_x, distance_y)
            lidar.update_tracker_heading(reading.x_angle, reading.y_angle)
            heading = lidar.get_heading()
            prevReading = [reading.x_angle, reading.y_angle,
                           heading, reading.x_dist, reading.y_dist]
            conn.send(prevReading)
        else:
            print("IF BLOCK NOT RAN")
            print(
                f"DX: {int(distance_x)}, DY: {int(distance_y)}, PX: {int(prevReading[3])}, PY: {int(prevReading[4])}")


def process_data(tracker, latest_data, lidar):
    t_angles = tracker.findCoordinates(latest_data)
    x = t_angles[0]
    y = t_angles[1]
    heading = lidar.get_heading()
    distance_x = latest_data[x]
    distance_y = latest_data[y]
    return Reading(x, y, heading, distance_x, distance_y)


if __name__ == '__main__':
    BaseManager.register('Lidar', Lidar)
    manager = BaseManager()
    manager.start()
    lidar_sensor = manager.Lidar('/dev/ttyUSB0')
    try:
        parent_conn, child_conn = multiprocessing.Pipe()
        p1 = multiprocessing.Process(target=sensor, args=(lidar_sensor,))
        p2 = multiprocessing.Process(target=robot_fb, args=(child_conn,))
        p3 = multiprocessing.Process(
            target=handleSensorData, args=(parent_conn, lidar_sensor))
        p4 = multiprocessing.Process(target=filter_data, args=(lidar_sensor,))
        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()

    except KeyboardInterrupt:
        lidar_sensor.clean()
        print("DONE")
