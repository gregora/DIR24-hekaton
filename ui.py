from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

import math

import sys


from pipeline import pipeline, demo
from TcpIP_client import Robot
from quality import quality

import time


# ifconfig enp1s0 10.131.42.54 netmask 255.0.0.0

robot = Robot()
rx, ry, rz = 9.27, -175, -90
z = -321

placed = {
    "small": 0,
    "medium": 0,
    "large": 0
}

startB = False

hostName = "localhost"
serverPort = 8080

def plan_a():
    print("Plan A")
    
    robot.client_send("StartA*")

    print("Plan A done")

    return True

def plan_b(size):

    print("Plan B - " + size)

    image, objects = pipeline(debug_show=False)

    #save image to web/test.png
    cv2.imwrite("web/test.png", image)

    for x, y, angle, width, height, area in objects:

        rz = angle + 180

        if rz > 180:
            rz -= 180

        calculation_angle = rz + 90
        calculation_angle = - calculation_angle

        #print("Calculation angle: " + str(calculation_angle))

        x_offset = 0  - math.sin(math.radians(calculation_angle)) * 70
        y_offset = 70 + math.cos(math.radians(calculation_angle)) * 70

        x_calibration_offset = -5.5
        y_calibration_offset = 0

        x_offset += x_calibration_offset
        y_offset += y_calibration_offset

        time.sleep(1)
        #print(x, y, angle, width, height, area)
        sizes = {
            200: "small",
            410: "medium",
            600: "large"
        }

        #find nearest number for area from 200, 400, 600
        nearest = min(sizes.keys(), key=lambda x: abs(x - area))

        if(sizes[nearest] == size):
            global startB
            placed[size] += 1
            if(not startB):
                robot.client_send("StartB*")
                startB = True
            print("Picking up " + sizes[nearest] + " object")
            print(str(x) + " " + str(y))

            robot.client_send_cords(x - x_offset, y - y_offset, z, rx, ry, rz)


            rec = ""
            while not "In position" in rec:    
                rec = robot.client_receive()

            camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            camera.set(10, 130)
            camera.set(11, 50)
            camera.set(15, 255)

            #print("Camera connected")

            return_value, image = camera.read()

            image, _ = pipeline(debug_show=False)


            cv2.imwrite("web/quality.png", image)

            q = quality(image)

            tb = q.orientation() #1 - top, 0 - bottom
            distance = q.qual()

            print("Distance: " + str(distance))

            product_ok = False

            if distance >= 5 and distance <= 29:
                product_ok = True

            if (product_ok):
                print("Product is okay!")
                robot.client_send("Ok*") #quality is okay

                #if tb == 0:
                #    if size == "medium":
                #       robot.client_send("Turn medium*")
                #    if size == "medium":
                #        robot.client_send("Turn large*")
                #    rec = ""
                #    while not "In position" in rec:    
                #        rec = robot.client_receive()

                #place = placed[size]
                #if size == "medium":
                #   if place == 1:
                #       robot.client_send("1*")
                #   if place == 2:
                #       robot.client_send("2*")
                #   if place == 3:
                #       robot.client_send("3*")
                #   if place == 4:
                #       robot.client_send("7*")
                #   if place == 5:
                #       robot.client_send("8*")

                #if size == "large":
                #   if place == 1:
                #       robot.client_send("4*")
                #   if place == 2:
                #       robot.client_send("5*")
                #   if place == 3:
                #       robot.client_send("6*")
                #   if place == 4:
                #       robot.client_send("9*")
                    

            else:
                print("WARNING: PRODUCT IS BROKEN!")
                robot.client_send("Brken*") #quality is not okay

            #robot.client_send("stop*")
            return True

    robot.client_send("stop*")
    return False


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/":
            self.path = "/index.html"
  
        if self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            f = open("web/index.html", "r")

            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

        if self.path.endswith(".png"):
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()

            f = open("web" + self.path, "rb")

            self.wfile.write(f.read())
            f.close()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode("utf-8")

        #print(post_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("POST request for " + self.path, "utf-8"))

        if post_data == "planA":
            result = plan_a()

        if "planB " in post_data:
            size = post_data.split(" ")[1]
            result = plan_b(size)

        if result:
            self.wfile.write(bytes("Success", "utf-8"))
        else:
            self.wfile.write(bytes("Failed", "utf-8"))





if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")







