import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class quality:
    def __init__(self, image):
        self.image = image
    def orientation(self):
        #Open image 
        self.canny = cv2.Canny(self.image, 150, 200)
        #crop image
        self.canny = self.canny[206:264, 301:347]

        #plt.imshow(self.canny, cmap='gray')
        #plt.show()

        kernel = np.ones((2,2), np.uint8)
        self.dialate = cv2.dilate(self.canny, kernel,iterations=1)

        #plt.figure(figsize=(10,10))
        #plt.imshow(self.dialate, cmap='gray')
        #plt.show()
        histogram = np.sum(self.dialate, axis=1)
        self.max_index = np.argmax(histogram)
        x_coords = np.where(self.canny[self.max_index, :] == 255)
        self.x_middle = int(np.round(np.median(x_coords)))
        #print(self.x_middle)
        #print(self.max_index)
        self.axis_y_len = len(histogram)
        #print(self.axis_y_len)
        if self.max_index < self.axis_y_len/2:
            #print("Top")
            return 1 
        else:
            #print("Bottom")
            return 0 
        

    def qual(self):
        #Crop the image from max indeks
        orient = self.orientation()
        if orient == 1:
            #Top side image
            self.dialate = self.dialate[self.max_index:,:]
            #Make a y histogram of left image from x_middle
            left = self.dialate[:,0:self.x_middle]
            right = self.dialate[:,self.x_middle:]

            # plt.figure(figsize=(10,10))
            # plt.subplot(1,2,1)
            # plt.imshow(left)
            # plt.subplot(1,2,2)
            # plt.imshow(right)
            # plt.show()
          
            bottom_left = left[left.shape[0]//2:, :]
            bottom_right = right[right.shape[0]//2:, :]

            brightest_pixel_left = np.unravel_index(np.argmax(bottom_left, axis=None), bottom_left.shape)
            brightest_pixel_right = np.unravel_index(np.argmax(bottom_right, axis=None), bottom_right.shape)
            brightest_pixel_left = (brightest_pixel_left[0] + left.shape[0]//2, brightest_pixel_left[1])
            brightest_pixel_right = (brightest_pixel_right[0] + right.shape[0]//2, brightest_pixel_right[1] + right.shape[1])

            # Calculate the distance between the two pixels
            distance = np.sqrt((brightest_pixel_right[0] - brightest_pixel_left[0])**2 + (brightest_pixel_right[1] - brightest_pixel_left[1])**2)

            #print(f"The distance between the brightest pixels is {distance} pixels")
            #TODO set quality value
            return distance

        else:
            #Bottom side image
            self.dialate = self.dialate[:self.max_index,:]
            left = self.dialate[:,0:self.x_middle]
            right = self.dialate[:,self.x_middle:]

            # plt.figure(figsize=(10,10))
            # plt.subplot(1,2,1)
            # plt.imshow(left)
            # plt.subplot(1,2,2)
            # plt.imshow(right)
            # plt.show()  
            #Bootom side image
            top_left = left[:left.shape[0]//2:, :]
            top_right = right[:right.shape[0]//2:, :]

            brightest_pixel_left = np.unravel_index(np.argmax(top_left, axis=None), top_left.shape)
            brightest_pixel_right = np.unravel_index(np.argmax(top_right, axis=None), top_right.shape)

            brightest_pixel_left = (brightest_pixel_left[0] + left.shape[0]//2, brightest_pixel_left[1])
            brightest_pixel_right = (brightest_pixel_right[0] + right.shape[0]//2, brightest_pixel_right[1] + right.shape[1])

            distance = np.sqrt((brightest_pixel_right[0] - brightest_pixel_left[0])**2 + (brightest_pixel_right[1] - brightest_pixel_left[1])**2)
            #print(f"The distance between the brightest pixels is {distance} pixels")

            return distance

        
        
        # plt.figure(figsize=(10,10))
        # plt.imshow(self.dialate, cmap='gray')
        # plt.show()
        

if __name__ == "__main__":
    img = cv2.imread('web/quality.png')

    plt.imshow(img)
    plt.show()

    q = quality(img)
    q.qual()

      