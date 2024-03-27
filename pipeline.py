import cv2
import numpy as np
import matplotlib.pyplot as plt

import sys

#image = cv2.imread(sys.argv[1])


#take a picture

def pipeline(debug_show = False):

    camera = cv2.VideoCapture(0)

    #camera settigs ids:
    # - brightness: 10
    # - contrast: 11
    # - saturation: 12
    # - hue: 13
    # - gain: 14
    # - exposure: 15

    camera.set(10, 130)

    return_value, image = camera.read()

    #use calibration.npz file to undistort image

    calibration = np.load('calibration.npz')
    mtx = calibration['mtx']
    dist = calibration['dist']

    rvecs = calibration['rvecs']
    tvecs = calibration['tvecs']

    image = cv2.undistort(image, mtx, dist, None, mtx)


    x1, y1 = 188, 25
    x2, y2 = 440, 31
    x3, y3 = 443, 203
    x4, y4 = 178, 196

    w, h = 300, 210

    pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    image_cropped = cv2.warpPerspective(image, matrix, (w, h))
    image_segments = image_cropped.copy()

    if debug_show:
        cv2.imshow('image_cropped', image_cropped)
    

    grey = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)


    #get treshold value using otsu

    #_, tresholded = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #tresholded = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    min_brightness = grey.min()
    grey = grey - min_brightness
    tresholded = np.where(grey > 3, 255, 0).astype(np.uint8)

    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(tresholded, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)


    segmented = cv2.connectedComponentsWithStats(dilated, 8, cv2.CV_32S)

    centers = segmented[3]
    centers = centers.astype(int)

    masks = []
    objects = []

    for i, center in enumerate(centers):

        if i == 0:
            continue

        area = segmented[2][i][4]
        
        mask = np.zeros_like(dilated)
        mask[segmented[1] == i] = 255

        #find outer contour of mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:

            contour_area = cv2.contourArea(c)

            if contour_area < 50:
                continue

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

            cv2.circle(image_cropped, (int(center_x), int(center_y)), 3, (0, 0, 255, 1), -1)
            cv2.drawContours(image_cropped, [box], 0, (255, 0, 0), 2)

            sizes = {
                200: (0, 0, 255),
                410: (0, 255, 0),
                600: (255, 0, 0)
            }

            #find nearest number for area from 200, 400, 600

            nearest = min(sizes.keys(), key=lambda x: abs(x - area))

            color = sizes[nearest]

            cv2.drawContours(image_segments, [box], 0, color, 2)

            # draw line to show angle
            x1 = int(center_x)
            y1 = int(center_y)
            x2 = int(center_x + 50 * np.cos(angle * np.pi / 180))
            y2 = int(center_y + 50 * np.sin(angle * np.pi / 180))

            cv2.line(image_cropped, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # transform center to original image
            cent = np.array([[center_x, center_y]], dtype=np.float32)
            cent = np.array([cent])

            matrix_inv = cv2.getPerspectiveTransform(pts2, pts1)
            cent = cv2.perspectiveTransform(cent, matrix_inv)

            center_x, center_y = cent[0][0]

            objects.append((center_x, center_y, angle, width, height, area))


        masks.append(mask)

    
    #unwarp cropping
    
    matrix_inv = cv2.getPerspectiveTransform(pts2, pts1)

    image_cropped = cv2.warpPerspective(image_cropped, matrix_inv, (image.shape[1], image.shape[0]))

    image = np.where(image_cropped > 0, image_cropped, image)

    #for o in objects:
    #    x, y, angle, width, height, area = o
    #    cv2.circle(image, (int(x), int(y)), 3, (255, 0, 0, 1), -1) #check if reverse transformation is correct

    if debug_show:
        cv2.imshow('image', image)
        cv2.imshow('segments', image_segments)

    return image, objects


def demo():

    while True:
        image, objects = pipeline(debug_show = True)

        #cv2.imshow('image', image)

        #print(np.array(objects))
        #print()
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
