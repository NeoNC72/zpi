import redis
import json

# Connect to Dragonfly (same as Redis connection)
dragonfly_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Add to the receive queue
def add_to_recv_queue(device_ip, message):
    queue_data = {"device_ip": device_ip, "message": message}
    dragonfly_client.lpush("recv_queue", json.dumps(queue_data))

# Process from the receive queue
def process_recv_queue():
    while True:
        data = dragonfly_client.rpop("recv_queue")
        if data:
            message = json.loads(data)
            # Process the message here
            print(f"Processing: {message}")
            # Add to send queue
            dragonfly_client.lpush("send_queue", json.dumps(message))
        else:
            break

# Send from the send queue
def send_from_send_queue():
    while True:
        data = dragonfly_client.rpop("send_queue")
        if data:
            message = json.loads(data)
            # Send the message to the device
            print(f"Sending: {message}")
        else:
            break

# Example usage
add_to_recv_queue("192.168.1.10", "Hello, device!")
process_recv_queue()
#send_from_send_queue()