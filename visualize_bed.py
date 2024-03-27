import numpy as np

import cv2

import matplotlib.pyplot as plt


base_x1, base_y1 = 313.34, -145.6
base_x2, base_y2 = 319.8, 154.69
base_x3, base_y3 = 528.5, 148.82
base_x4, base_y4 = 519.5, -147.40


# plot the four base points

plt.plot(base_x1, base_y1, 'ro')
plt.plot(base_x2, base_y2, 'ro')
plt.plot(base_x3, base_y3, 'ro')
plt.plot(base_x4, base_y4, 'ro')

plt.plot([base_x1, base_x2], [base_y1, base_y2], 'r-')
plt.plot([base_x2, base_x3], [base_y2, base_y3], 'r-')
plt.plot([base_x3, base_x4], [base_y3, base_y4], 'r-')
plt.plot([base_x4, base_x1], [base_y4, base_y1], 'r-')

plt.show()