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
        self.canny = self.canny[200:260, 230:280]
        kernel = np.ones((2,2), np.uint8)
        self.dialate = cv2.dilate(self.canny, kernel,iterations=1)

        plt.figure(figsize=(10,10))
        plt.imshow(self.dialate, cmap='gray')
        plt.show()
        histogram = np.sum(self.dialate, axis=1)
        self.max_index = np.argmax(histogram)
        x_coords = np.where(self.canny[self.max_index, :] == 255)
        self.x_middle = int(np.round(np.median(x_coords)))
        print(self.x_middle)
        print(self.max_index)
        self.axis_y_len = len(histogram)
        print(self.axis_y_len)
        if self.max_index < self.axis_y_len/2:
            print("Top")
            return 1 
        else:
            print("Bottom")
            return 0 
        

    def qual(self):
        #Crop the image from max indeks
        orient = self.orientation()
        if orient == 1:
            pass

        else:
            #Bootom side image
            self.dialate = self.dialate[0:self.max_index,:]
            pass
        
        plt.figure(figsize=(10,10))
        
        plt.imshow(self.dialate, cmap='gray')
        plt.show()
        


if __name__ == "__main__":
    img = cv2.imread('quality2.png')
    q = quality(img)
    q.qual()

      