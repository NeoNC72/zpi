import socket
import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

UDP_IP = "192.168.244.15"
UDP_PORT = 558

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT} recv_data.py")

while True:
    data, addr = sock.recvfrom(1024)
    if data.decode("utf-8") == "get_ip:;:0":
        sock.sendto(addr[0].encode(), addr)
    else:
        data_t_s = {"device_ip": addr[0], "device_port": addr[1], "message": data.decode()}
        print(f"Received message: {data}")
        redis_client.lpush("recv_queue", json.dumps(data_t_s))
    
