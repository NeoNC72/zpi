import redis
import json
import random
import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("192.168.244.15", 559)

sock.bind(addr)





def random_ip():
    x = ".".join(str(random.randint(0, 255)) for _ in range(4))
    x = x + "_dont_exist"
    return x
def random_port():
    return random.randint(0, 65535)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

redis_client.lpush("recv_queue", json.dumps({"device_ip": addr[0], "device_port": addr[1], "message": "register_id:;:788"}))
ips = []
for i in range(800, 850):
    ips.append((random_ip(), random_port()))
for i in range(800, 850):
    redis_client.lpush("recv_queue", json.dumps({"device_ip": ips[i-800][0], "device_port": ips[i-800][1], "message": f"register_id:;:{i}"}))
ans = ["A", "B", "C"]

while True:
    data, addr = sock.recvfrom(60000)
    
    print(f"Received: {data}")
    datas = data.decode().split(":;:")
    if datas[0] == "question":
        redis_client.lpush("recv_queue", json.dumps({"device_ip": addr[0], "device_port": addr[1], "message": f"ack_q:;:788"}))
        for i in range(800, 850):
            redis_client.lpush("recv_queue", json.dumps({"device_ip": ips[i-800][0], "device_port": ips[i-800][1], "message": f"ack_q:;:{i}"}))
        time.sleep(5)
        time.sleep(0.2)
        redis_client.lpush("recv_queue", json.dumps({"device_ip": addr[0], "device_port": addr[1], "message": f"answer:;:788:;:{random.choice(ans)}"}))
        for i in range(800, 850):
            redis_client.lpush("recv_queue", json.dumps({"device_ip": ips[i-800][0], "device_port": ips[i-800][1], "message": f"answer:;:{i}:;:{random.choice(ans)}"}))
