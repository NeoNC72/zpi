import socket

UDP_IP = "192.168.244.15"
UDP_PORT = 558

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendsock.bind((UDP_IP, 559))

test_s = set()
ips = set()

print(f"Listening on {UDP_IP}:{UDP_PORT}")
while True:
    data, addr = sock.recvfrom(1024)
    d = data.decode()
    print(f"Received message: {data} from {addr}")
    spl = d.split(":;:")
    print(spl)
    if spl[0] == "register_id":
        
        if spl[1] not in test_s:
            test_s.add(spl[1])
            sock.sendto("valid".encode(), addr)
            ips.add(addr[0])
        else:
            sock.sendto("ID taken".encode(), addr)
    elif spl[0] == "get_ip":
        sock.sendto(addr[0].encode(), addr)
    """
    for i in ips:
        sock.settimeout(5)
        try:
            sendsock.sendto("alive".encode(), (i, 559))
            data, addr = sock.recvfrom(1024)
            if data.decode() == "alive":
                print(f"Client {i} is alive")
        except socket.timeout:
            print(f"Client {i} is dead")
            ips.remove(i)
        sock.settimeout(None)
    """
    



