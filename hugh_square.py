import cv2
import numpy as np

import matplotlib.pyplot as plt

import sys


def hugh_square(image, square_w, square_h):
    #image has to be binary (black and white)

    n, m = image.shape

    #resize image to be 10x smaller
    image = cv2.resize(image, (int(n/10), int(m/10)))

    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')

    n, m = image.shape

    #position x, y and orientation theta
    votes = np.zeros((n, m, 180))

    for i in range(n):
        for j in range(m):
            if image[i, j] == 255:
                for theta in range(180):
                    x = i - square_w * np.cos(theta)
                    y = j - square_h * np.sin(theta)
                    if 0 <= x < n and 0 <= y < m:
                        votes[int(x), int(y), theta] += 1

    max_votes = np.max(votes)

    plt.subplot(1, 2, 2)
    plt.imshow(votes[:, :, 30], cmap='gray')
    plt.show()

hugh_square(cv2.imread('tresholded.png', 0), 5, 5)