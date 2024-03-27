import cv2
import numpy as np
import matplotlib.pyplot as plt

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

x, y, angle, width, height, area = objects[0]

print(x, y, angle, width, height, area)


# DANGER
robot.client_send("StartA*")
# robot.client_send_cords(x, y, z, rx, ry, rz)


#robot.close_socket()


time.sleep(20)
