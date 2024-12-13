import socket

UDP_IP = "192.168.244.15"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data = input("Enter message: ")
    sock.sendto(data.encode(), (UDP_IP, 558))