import cv2
import numpy as np
import matplotlib.pyplot as plt

import math

import sys


from pipeline import pipeline, demo
from TcpIP_client import Robot

import time


#image, objects = pipeline()
#objects = np.array(objects)
#print(objects)

rx, ry, rz = 9.27, -175, -90
z = -321

robot = Robot()


image, objects = pipeline(debug_show=True)

#time.sleep(1)

robot.client_send("StartB*")

for x, y, angle, width, height, area in objects:

    rz = angle + 180

    if rz > 180:
        rz -= 180

    calculation_angle = rz + 90
    calculation_angle = - calculation_angle

    print("Calculation angle: " + str(calculation_angle))

    x_offset = 0  - math.sin(math.radians(calculation_angle)) * 70
    y_offset = 70 + math.cos(math.radians(calculation_angle)) * 70

    x_calibration_offset = -5.5
    y_calibration_offset = 0

    x_offset += x_calibration_offset
    y_offset += y_calibration_offset

    time.sleep(1)
    print(x, y, angle, width, height, area)
    sizes = {
        200: "small",
        410: "medium",
        600: "large"
    }

    #find nearest number for area from 200, 400, 600
    nearest = min(sizes.keys(), key=lambda x: abs(x - area))

    print("Picking up " + sizes[nearest] + " object")
    print(str(x) + " " + str(y))

    robot.client_send_cords(x - x_offset, y - y_offset, z, rx, ry, rz)
    time.sleep(30)

robot.client_send("stop*")

robot.close_socket()
