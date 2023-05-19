import RPi.GPIO as GPIO
import numpy as np
from math import cos, sin, pi
from line import Line
from point import Point
from util import get_perpendicular_distance
from tracker import Tracker
from lidar.reading import Reading
from time import sleep
from motor import Motor
import time

sample_path = [Line(start=Point(2057, 2057, covered=True), end=Point(2057, 508, is_start=False)),
               Line(start=Point(1346, 1700), end=Point(
                   1346, 508, is_start=False)),
               Line(start=Point(757, 1700), end=Point(757, 508, is_start=False))]


class Robot:
    def __init__(self, path):
        self.motor_a = Motor(25, 23, 24, 15000, 0)
        self.motor_b = Motor(22, 17, 27, 15000, 0)
        self.motor_c = Motor(21, 20, 16, 15000, 0)
        self.motor_d = Motor(26, 19, 6, 15000, 0)
        self.path_lines = path.get_path()
        self.robot_at_start_of_line = True
        self.current_line = self.path_lines[0]
        self.current_line_index = 0
        self._path_len = len(self.path_lines)
        self.target_point = self.current_line.start
        self.start_to_end = True
        self.target_point_is_end = False
        self.prev_time = time.time()
        self.lastXerror = 0.0
        self.lastYerror = 0.0
        self.lastThetaError = 0.0

        self.intXerror = 0.0
        self.intYerror = 0.0
        self.intThetaError = 0.0

    def _move_all_motors(self):
        self.motor_a.rotate_forward()
        self.motor_b.rotate_forward()
        self.motor_c.rotate_forward()
        self.motor_d.rotate_forward()

    def _move_all_motors_back(self):
        self.motor_a.rotate_backward()
        self.motor_b.rotate_backward()
        self.motor_c.rotate_backward()
        self.motor_d.rotate_backward()

    def _stop_all_motors(self):
        self.motor_a.stop()
        self.motor_b.stop()
        self.motor_c.stop()
        self.motor_d.stop()

    def find_to_next_point(self):
        print('RUNNING FINDING NEXT POINT')
        try:
            if self.current_line_index < self._path_len:
                if self.target_point.is_start:
                    if self.current_line.end.covered:
                        self.current_line_index += 1
                        self.current_line = self.path_lines[self.current_line_index]
                        self.target_point = self.current_line.start
                    else:
                        self.target_point = self.current_line.end
                else:
                    if self.current_line.start.covered:
                        self.current_line_index += 1
                        self.current_line = self.path_lines[self.current_line_index]
                        self.target_point = self.current_line.end
                    else:
                        self.target_point = self.current_line.start
            else:
                print("Robot Path Completed")
                self._stop_all_motors()
                time.sleep(15)
        except IndexError:
            print("Robot Path Completed")
            self._stop_all_motors()
            time.sleep(15)

    def plant(self, xError, yError, thetaError, heading):
        r = 35.56
        l = 203
        w = 230/2
        kpLinearX = 3
        kpLinearY = 5
        kpAngular = 3.5
        thetaDot = kpAngular*thetaError
        theta = heading
        if abs(xError) > 500:
            if xError < 0:
                xError = -500
            else:
                xError = 500
        xDot = kpLinearX * xError
        if abs(yError) > 500:
            if yError < 0:
                yError = -500
            else:
                yError = 500
        yDot = kpLinearY * yError
        theta = pi*theta/180
        current_time = time.time()
        dt = current_time - self.prev_time
        if (self.lastXerror == 0.0) and (self.lastYerror == 0.0):
            kdLinear = 0
            kdAngular = 0
        else:
            kdLinear = 20000
            kdAngular = 50
        kiLinear = 0
        kiAngular = 0
        xDot = xDot + kdLinear * \
            ((xError - self.lastXerror)/dt) + kiLinear*(self.intXerror)
        yDot = yDot + kdLinear * \
            ((yError - self.lastYerror)/dt) + kiLinear*(self.intYerror)
        thetaDot = thetaDot + kdAngular * \
            ((thetaError - self.lastThetaError)/dt) + \
            kiAngular*(self.intThetaError)
        self.lastXerror = xError
        self.lastYerror = yError
        self.lastThetaError = thetaError
        self.intXerror = self.intXerror + (xError*dt)
        self.intYerror = self.intYerror + (yError*dt)
        self.intThetaError = self.intThetaError + (thetaError*dt)
        M = np.matrix([[cos(theta)+sin(theta), sin(theta)-cos(theta), -w-l],
                       [cos(theta)-sin(theta), cos(theta)+sin(theta), w+l],
                       [cos(theta)+sin(theta), sin(theta)-cos(theta), w],
                       [cos(theta)-sin(theta), sin(theta)+cos(theta), w]])

        d = [xDot, yDot, thetaDot]

        wheelSpeeds = (1/r)*(np.matmul(M, d))
        self.prev_time = current_time
        return wheelSpeeds

    def _move_robot_to_point(self, current_data):
        position_x, position_y = current_data.x_dist, current_data.y_dist
        print(
            f"TARGET: {self.target_point.x}, {self.target_point.y}, {self.target_point.covered}")
        xError = -(position_x - self.target_point.x)
        yError = -(position_y - self.target_point.y)
        # if current_position is within the target point, we find the next point
        if abs(xError) <= 50 and abs(yError) <= 50:
            self.target_point.covered = True
            self.find_to_next_point()
        else:
            xError = -(position_x - self.target_point.x)
            yError = -(position_y - self.target_point.y)
            # print(f"X_ERROR: {xError}")
            # print(f"Y_ERROR: {yError}")
            # print(f"HEADING: {current_data.heading}")
            if current_data.heading > 180:
                thetaError = 360 - current_data.heading
            else:
                thetaError = -current_data.heading
            thetaError = pi*thetaError/180
            speedRequirements = self.plant(
                xError, yError, thetaError, current_data.heading)
            # Speed requirements [speed A, Speed D, Speed, C, Speed b]

            # Run neccessary calculations and motor commands
            # Move the robot from curren_position towards target point
            if abs(speedRequirements.item(0)) < 0.1:
                duty_cycle_A = 0
            else:
                duty_cycle_A = 17.282 * \
                    (abs(1/speedRequirements.item(0)))**(-0.992)
            if abs(speedRequirements.item(3)) < 0.1:
                duty_cycle_B = 0
            else:
                duty_cycle_B = 18.8 * \
                    (abs(1/speedRequirements.item(3)))**(-1.032)
            if abs(speedRequirements.item(2)) < 0.1:
                duty_cycle_C = 0
            else:
                duty_cycle_C = 23.169 * \
                    (abs(1/speedRequirements.item(2)))**(-1.081)
            if abs(speedRequirements.item(1)) < 0.1:
                duty_cycle_D = 0
            else:
                duty_cycle_D = 51.44 * \
                    (abs(1/speedRequirements.item(1)))**(-1.252)

            spds = [speedRequirements.item(0),
                    speedRequirements.item(3),
                    speedRequirements.item(2),
                    speedRequirements.item(1)]
            # print(f"SPEEDS: {spds}")
            # print(
            #     f"DC: {[duty_cycle_A, duty_cycle_B, duty_cycle_C, duty_cycle_D]}")
            if duty_cycle_A >= 100:
                duty_cycle_A = 99
            if duty_cycle_B >= 100:
                duty_cycle_B = 99
            if duty_cycle_C >= 100:
                duty_cycle_C = 99
            if duty_cycle_D >= 100:
                duty_cycle_D = 99

            if speedRequirements.item(0) > 0:
                if duty_cycle_A >= 100:
                    duty_cycle_A = 99
                self.motor_a.change_speed(duty_cycle_A)
                self.motor_a.rotate_forward()
            else:
                self.motor_a.change_speed(duty_cycle_A)
                self.motor_a.rotate_backward()

            if speedRequirements.item(3) > 0:
                self.motor_b.change_speed(duty_cycle_B)
                self.motor_b.rotate_forward()
            else:
                self.motor_b.change_speed(duty_cycle_B)
                self.motor_b.rotate_backward()

            if speedRequirements.item(2) > 0:
                self.motor_c.change_speed(duty_cycle_C)
                self.motor_c.rotate_forward()
            else:
                self.motor_c.change_speed(duty_cycle_C)
                self.motor_c.rotate_backward()

            if speedRequirements.item(1) > 0:
                self.motor_d.change_speed(duty_cycle_D)
                self.motor_d.rotate_forward()
            else:
                self.motor_d.change_speed(duty_cycle_D)
                self.motor_d.rotate_backward()

    def rf(self):
        duty = 10
        while True:
            self._move_all_motors()
            sleep(2.5)
            duty += 10
            self.motor_a.change_speed(duty)
            self.motor_b.change_speed(duty)
            self.motor_c.change_speed(duty)
            self.motor_d.change_speed(duty)
            if duty == 100:
                duty = 10

    def end(self):
        GPIO.cleanup()

    def controller(self, prevReading):
        sensor_readings = Reading(
            prevReading[0], prevReading[1], prevReading[2], prevReading[3], prevReading[4])
        self._move_robot_to_point(sensor_readings)
