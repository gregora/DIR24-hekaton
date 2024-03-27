# TCP/IP Communication with Robot 

# Step 1: Set a Static IP Address on the Computer
# Ensure your computer's IP address is in the same subnet as the robot's IP address.

# Step 2: Configure the Robot's Network Settings (Optional)
# If required, configure the robot's network settings to ensure it can communicate on your network.

# Step 3: Run the Application on the Robot

# Step 4: Run the Script on the PC
# Execute your communication script. This script will connect to the robot and allow for message exchange.

# Step 5: Send and Receive Messages
# Messages end with a specific delimiter ("*").


import socket
import time
import signal

class Robot:

    def __init__(self) -> None:            
        self.HOST = "10.131.42.55"     #server, in this case the robot
        self.PORT = 2000  #reserved ports for TCP/IP on the robot are: 1-1000

        print("Connecting...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST,self.PORT))

    def client_send(self, msg_s):
        print("Sending: " + msg_s + "\n")
        #msg_bytes = int(msg_s).to_bytes(1, 'big') #to_bytes accepts only integers!!!
        msg_e = msg_s.encode('utf-8')             #can we avoid encoding to bytes?
    
        self.sock.sendall(msg_e)
        
        time.sleep(1)
        
        
    def client_receive(self):
        msg_d, addr = self.sock.recvfrom(1024)
        msg_r = msg_d.decode('utf-8')        #data needs to be decoded first
        
        print("Received: " + msg_r)


    def client_send_cords(self, x, y, z, rx, ry, rz):
        msg = str(x) + " " + str(y) + " " + str(z) + " " + str(rx) + " " + str(ry) + " " + str(rz) +"*"
        self.client_send(msg)

    def close_socket(self):
        print("Closing socket ...")
        self.socket.close()
        print("Socket closed!")

#client_send_cords(340, -202)

def test():

    def handler(signal, frame):
        robot.close_socket()

    signal.signal(signal.SIGINT, handler)

    print("Welcome to Gregor's AMAZING script")

    while True:
    
        robot = Robot()
    
        data_s = input("Send: ")
        robot.client_send(data_s)
        
        #coords = input("Coords: ")
        #x, y = coords.split(" ")
        #x = int(x)
        #y = int(y)
        #client_send_cords(x, y)

        data_r = robot.client_receive()
        print(data_r)
        
