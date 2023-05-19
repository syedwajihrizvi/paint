# Date: July 5 2022
# Decode the Sample File and collect all Autocad functions and find meaning of them
# Figure out what these symbols mean by sraping web and getting their definition
import RPi.GPIO as GPIO
from bs4 import BeautifulSoup
from pprint import pprint

from line import Line
# from path import Path
# from dxf import DXF_Editor
from motor import Motor
from robot import Robot

# This function collects all the symbols from the sample test file
motorA = Motor(25, 23, 24, 1000, 10)
motorB = Motor(22, 17, 27, 1000, 10)
motorC = Motor(21, 20, 16, 1000, 10)
motorD = Motor(26, 19, 6, 1000, 10)

try:
    motorA.stop()
    motorB.stop()
    motorC.stop()
    motorD.stop()
    while True:
        x = input()
        print("X: " + x)

        if x == "f":
            motorA.rotate_forward()
            motorB.rotate_forward()
            motorC.rotate_forward()
            motorD.rotate_forward()

        if x == "h":
            motorA.rotate_forward()
            motorB.rotate_backward()
            motorC.rotate_forward()
            motorD.rotate_backward()

        if x == "z":
            motorA.rotate_forward()
            motorB.stop()
            motorC.rotate_forward()
            motorD.stop()

        if x == "w":
            motorA.stop()
            motorB.rotate_forward()
            motorC.stop()
            motorD.rotate_forward()

        elif x == "b":
            motorA.rotate_backward()
            motorB.rotate_backward()
            motorC.rotate_backward()
            motorD.rotate_backward()

        elif x == "s":
            motorA.stop()
            motorB.stop()
            motorC.stop()
            motorD.stop()

        elif "D" in x:
            y = int(x[1:])
            motorA.change_speed(1*y)
            motorB.change_speed(1*y)
            motorC.change_speed(1*y)
            motorD.change_speed(1*y)

        elif "FR" in x:
            y = int(x[2:])
            motorA.p.ChangeFrequency(1*y)
            motorB.p.ChangeFrequency(1*y)
            motorC.p.ChangeFrequency(y)
            motorD.p.ChangeFrequency(y)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
