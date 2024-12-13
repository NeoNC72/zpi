import redis
import json 
import time
old_time = 0
def get_curr_device_state():
    curr_device_state = redis_client.json().get("device_state")
    if curr_device_state:
        return json.loads(curr_device_state)
    else:
        return {}

def get_state():
    state = redis_client.json().get("state")
    if state:
        return json.loads(state)
    else:
        return {}

def get_curr_devices():
    curr_devices = redis_client.json().get("devices")
    if curr_devices:
        return json.loads(curr_devices)
    else:
        return []
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


while True:
    curr_devices = get_curr_device_state()
    curr_ids = get_curr_devices()
    for j in curr_ids:
        if j not in curr_devices:
            curr_ids.remove(j)
            print(f"Device {j} has been removed")
    if curr_ids != get_curr_devices():
        redis_client.json().set("devices", ".", json.dumps(curr_ids))
        
    for i in curr_devices:
        

        data = curr_devices[i]
        if "acked" in data:
            if data["acked"] == False:
                print(f"Device {data['ip']}({i}) has not acked")
                if data["time"] + 5 < time.time():
                    print(f"Device {data['ip']} has not acked in time")
                    redis_client.lpush("recv_queue", json.dumps({"device_ip": data["ip"], "device_port": 777, "message": "delete:;:" + i}))
                    redis_client.hset("answered", "total", int(redis_client.hget("answered", "total")) - 1)
    state = get_state()
    if "timer" not in state or "running" not in state:
        pass
    else:
        if state["running"] == True:
            new_time = state["timer"]
            if new_time == old_time:
                    redis_client.lpush("recv_queue", json.dumps({"device_ip": "dont", "device_port": 123, "message": "time:;:0"}))
            old_time = new_time
        
            if state["timer"] <=0 or (int(redis_client.hget("answered", "did")) == int(redis_client.hget("answered", "total"))):
                print("Time is up!")
                redis_client.lpush("recv_queue", json.dumps({"device_ip": "dont", "device_port": 123, "message": "end"}))
                for i in curr_devices:
                    redis_client.hset("answered", "did", 0)
                    redis_client.hset("answered", "total", 0)
    
    time.sleep(1)
    