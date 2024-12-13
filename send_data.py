import socket
import redis
import json


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


UDP_IP = "192.168.244.15"
UDP_PORT = 560

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT} send_data.py")

while True:
    data = redis_client.rpop("send_queue")
    
    if data:
        data = json.loads(data.decode("utf-8"))
        dest_ip = data["device_ip"]
        if dest_ip.endswith("_dont_exist"):
            continue
        dest_port = data["device_port"]
        dest_data = data["message"]
        print(f"Sending message: {dest_data} to {dest_ip}:{dest_port}")
        sock.sendto(dest_data.encode(), (dest_ip, dest_port))
    else:
        pass