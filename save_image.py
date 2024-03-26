import cv2
import numpy as np
import matplotlib.pyplot as plt

import sys

name = sys.argv[1]

def save_picture(name):

    camera = cv2.VideoCapture(2)

    #camera settigs ids:
    # - brightness: 10
    # - contrast: 11
    # - saturation: 12
    # - hue: 13
    # - gain: 14
    # - exposure: 15


    camera.set(10, 150)

    return_value, image = camera.read()


    cv2.imwrite(name, image)
    del(camera)

save_picture(name)