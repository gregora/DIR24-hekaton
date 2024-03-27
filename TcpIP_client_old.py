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

HOST = "10.131.42.55"     #server, in this case the robot
PORT = 2000  #reserved ports for TCP/IP on the robot are: 1-1000

print("Connecting...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

def client_send(msg_s):
    print("Sending: " + msg_s + "\n")
    #msg_bytes = int(msg_s).to_bytes(1, 'big') #to_bytes accepts only integers!!!
    msg_e = msg_s.encode('utf-8')             #can we avoid encoding to bytes?
 
    sock.sendall(msg_e)
    
    time.sleep(1)
    
    
def client_receive():
    msg_d, addr = sock.recvfrom(1024)
    msg_r = msg_d.decode('utf-8')        #data needs to be decoded first
    
    print("Received: " + msg_r)
    

while True:
    print("Send: ")
    data_s = input()
    client_send(data_s)
    
    data_r = client_receive()
    
