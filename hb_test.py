import socket
import time

UDP_IP = "192.168.244.15"
UDP_PORT = 559

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

test_s = set()
addr = ('192.168.244.196', 559)

while True:
    time.sleep(1)
    sock.settimeout(5)
    try:
        sock.sendto("alive".encode(), addr)
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data} from {addr}")
    except socket.timeout:
        print("Timeout")
        continue
    

