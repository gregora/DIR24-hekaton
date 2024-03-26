import cv2
import numpy as np
import matplotlib.pyplot as plt


def take_a_picture(simulated = False):

    if(simulated):
        image = cv2.imread('image8.png')
        return image

    camera = cv2.VideoCapture(2)
    return_value, image = camera.read()

    return image

def save_picture(name):

    camera = cv2.VideoCapture(2)
    return_value, image = camera.read()
    cv2.imwrite(name, image)
    del(camera)

def edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    return edges

image = take_a_picture(simulated = True)

plt.subplot(3, 3, 1)
plt.imshow(image)

plt.subplot(3, 3, 2)
edg = edges(image)
plt.imshow(edg)

plt.subplot(3, 3, 3)
image_hsb = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
plt.imshow(image_hsb)

plt.subplot(3, 3, 4)
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#blob detection
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 0
params.filterByCircularity = True
params.minCircularity = 0.1
params.filterByConvexity = True
params.minConvexity = 0.1
params.filterByInertia = True
params.minInertiaRatio = 0.01
params.filterByColor = False
detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(edg)

print(keypoints)

im_with_keypoints = cv2.drawKeypoints(grey, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.imshow(im_with_keypoints)

plt.subplot(3, 3, 5)
#contours

contours, hierarchy = cv2.findContours(edg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

plt.imshow(image)

plt.subplot(3, 3, 6)

plt.imshow(grey, cmap='gray')

plt.subplot(3, 3, 7)

#treshold grey image and show result

tresholded = np.where(grey > 5, 255, 0)
tresholded = np.uint8(tresholded)

#save tresholded image
cv2.imwrite('tresholded.png', tresholded)

plt.imshow(tresholded, cmap='gray')

plt.subplot(3, 3, 8)

#detect rectangles using blob detection

keypoints = detector.detect(tresholded)

im_with_keypoints = cv2.drawKeypoints(grey, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.imshow(im_with_keypoints)

plt.subplot(3, 3, 9)

#erode and dilate image

kernel = np.ones((10, 10), np.uint8)
eroded = cv2.erode(tresholded, kernel, iterations=1)
dilated = cv2.dilate(eroded, kernel, iterations=1)

cv2.imwrite('denoised.png', dilated)

plt.imshow(dilated, cmap='gray')

plt.show()



#segment image


segmented = cv2.connectedComponentsWithStats(dilated, 8, cv2.CV_32S)


plt.subplot(3, 3, 1)
plt.imshow(segmented[1], cmap='gray')

plt.subplot(3, 3, 2)

#print centers

centers = segmented[3]
centers = centers.astype(int)

masks = []

for i, center in enumerate(centers):

    if i == 0:
        continue

    area = segmented[2][i][4]
    print("Area of " + str(i) + " is: " + str(area))
    
    cv2.circle(image, (center[0], center[1]), 5, (0, 0, 255, 1), -1)

    mask = np.zeros_like(dilated)
    mask[segmented[1] == i] = 255

    #find outer contour of mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        
        #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        rect = cv2.minAreaRect(c)

        angle = rect[2]
        center_x, center_y = rect[0]
        width, height = rect[1]

        if height > width:
            angle += 90

        #draw min area rectangle

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(image, [box], 0, (255, 0, 0), 2)

        # draw line to show angle
        x1 = int(center_x)
        y1 = int(center_y)
        x2 = int(center_x + 50 * np.cos(angle * np.pi / 180))
        y2 = int(center_y + 50 * np.sin(angle * np.pi / 180))

        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


    masks.append(mask)

plt.imshow(image)

plt.show()