from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

import math

import sys


from pipeline import pipeline, demo
from TcpIP_client import Robot

import time


# ifconfig enp1s0 10.131.42.54 netmask 255.0.0.0

robot = Robot()
rx, ry, rz = 9.27, -175, -90
z = -321


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

            robot.client_send("StartB*")
            print("Picking up " + sizes[nearest] + " object")
            print(str(x) + " " + str(y))

            robot.client_send_cords(x - x_offset, y - y_offset, z, rx, ry, rz)

            rec = robot.client_receive()
            print("Received: " + rec)

            robot.client_send("Ok*") #quality is okay
            
            robot.client_send("stop*")
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







