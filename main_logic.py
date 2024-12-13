import redis
import json
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def make_results():
    sort_list = []
    curr_devices = get_curr_device_state()
    state = get_state()
    
    correct = state["correct"]
    
    for d in curr_devices:
        if curr_devices[d]["answered"] == True:
            if curr_devices[d]["answer"] == correct:
                sort_list.append((1, curr_devices[d]["time_taken"], d))
            else:
                sort_list.append((2, curr_devices[d]["time_taken"], d))
    sort_list.sort()
    ret_s = f"{correct}"
    for i in range(len(sort_list)):
        ret_s += f";{i + 1}.: {sort_list[i][2]}X{round(sort_list[i][1], 2)}s ({curr_devices[sort_list[i][2]]['answer']})"
    
    return ret_s

def get_curr_devices():
    curr_devices = redis_client.json().get("devices")
    if curr_devices:
        return json.loads(curr_devices)
    else:
        return []

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

def check_and_add_ips(device_state, ip, id, curr_devices):
    removal = []
    for d in device_state:
        if device_state[d]["ip"] == ip:
            removal.append(d)
    
    for r in removal:

        del device_state[r]
    
    
    
    device_state[id] = {"ip": ip}
            

while True:
    data = redis_client.rpop("recv_queue")
    if data:
        print(f"Received message: {data}")
        message = json.loads(data.decode("utf-8"))
        print(f"Processing: {message}")
        msg = message["message"]
        ip = message["device_ip"]
        port = 559
        
        spl = msg.split(":;:")
        
        if spl[0] == "register_id":
            curr_devices = get_curr_devices()
            device_state = get_curr_device_state()
            if spl[1] not in curr_devices:
                
                
                check_and_add_ips(device_state, ip, spl[1], curr_devices)
                
                curr_devices.append(spl[1])
                redis_client.json().set("devices", "." ,json.dumps(curr_devices))
                redis_client.json().set("device_state", "." ,json.dumps(device_state))
                redis_client.lpush("send_queue", json.dumps({"device_ip": message["device_ip"], "device_port": port, "message": "valid"}))
            else:
                redis_client.lpush("send_queue", json.dumps({"device_ip": message["device_ip"], "device_port": port, "message": "ID taken"}))
        elif spl[0] == "get_ip":
            redis_client.lpush("send_queue", json.dumps({"device_ip": message["device_ip"], "device_port": port, "message": message["device_ip"]}))
        
        elif spl[0] == "new_question":
            curr_devices = get_curr_device_state()
            state = get_state()
            should_run = True
            if "running" in state:
                if state["running"] == True:
                    should_run = False
            if should_run:
                state["running"] = True
                state["question"] = spl[1]
                state["answers"] = spl[4:]
                state["correct"] = spl[2]
                state["timer"] = int(spl[3])
                state["timer_stay"] = int(spl[3])
                state["start_time"] = time.time()
                redis_client.json().set("state", "." ,json.dumps(state))
                redis_client.hset("answered", "did", 0)
                redis_client.hset("answered", "total", 0)
                for d in curr_devices:
                    print(f"Sending question to {d}")
                    redis_client.lpush("send_queue", json.dumps({"device_ip": curr_devices[d]["ip"], "device_port": 559, "message": f"question:;:{spl[1]}:;:{spl[4]}:;:{spl[5]}:;:{spl[6]}"}))
                    curr_devices[d]["acked"] = False
                    curr_devices[d]["answered"] = False
                    curr_devices[d]["answer"] = None
                    curr_devices[d]["time"] = time.time()
                    redis_client.json().set("device_state", "." ,json.dumps(curr_devices))
                    redis_client.hset("answered", "total", int(redis_client.hget("answered", "total")) + 1)
        
        elif spl[0] == "ack_q":
            curr_devices = get_curr_device_state()
            curr_devices[spl[1]]["acked"] = True
            redis_client.json().set("device_state", ".", json.dumps(curr_devices))
            
        elif spl[0] == "answer":
            curr_devices = get_curr_device_state()
            curr_devices[spl[1]]["answered"] = True
            curr_devices[spl[1]]["answer"] = spl[2]
            curr_devices[spl[1]]["time_taken"] = time.time() - curr_devices[spl[1]]["time"]
            redis_client.json().set("device_state", "." ,json.dumps(curr_devices))
            redis_client.hset("answered", "did", int(redis_client.hget("answered", "did")) + 1)
            
            for d in curr_devices:
                if curr_devices[d]["answered"] == True:
                    redis_client.lpush("send_queue", json.dumps({"device_ip": curr_devices[d]["ip"], "device_port": 559, "message": f"{redis_client.hget('answered', 'did').decode('utf-8')}/{redis_client.hget('answered', 'total').decode('utf-8')}"}))
        
        elif spl[0] == "end":
            state = get_state()
            state["running"] = False
            redis_client.json().set("state", "." ,json.dumps(state))
            curr_devices = get_curr_device_state()

            time.sleep(1)
            for d in curr_devices:
                redis_client.lpush("send_queue", json.dumps({"device_ip": curr_devices[d]["ip"], "device_port": 559, "message": f"done"}))
                

        elif spl[0] == "time":
            state = get_state()
            took = time.time() - state["start_time"]
            
            state["timer"] = state["timer_stay"] - took
            redis_client.json().set("state", "." ,json.dumps(state))
            curr_devices = get_curr_device_state()
            if ip != "dont":
                if state["timer"] <= 0:
                    redis_client.lpush("send_queue", json.dumps({"device_ip": ip, "device_port": 559, "message": f"END"}))
                else:
                    redis_client.lpush("send_queue", json.dumps({"device_ip": ip, "device_port": 559, "message": f"{time.strftime('%M:%S', time.gmtime(state['timer']))}"}))        

        elif spl[0] == "results":
            curr_devices = get_curr_device_state()
            results = make_results()
            for d in curr_devices:
                redis_client.lpush("send_queue", json.dumps({"device_ip": curr_devices[d]["ip"], "device_port": 559, "message": results}))
        
        elif spl[0] == "delete":
            if spl[1] in get_curr_devices():
                curr_devices = get_curr_devices()
                device_state = get_curr_device_state()
                curr_devices.remove(spl[1])
                del device_state[spl[1]]
                redis_client.json().set("devices", "." ,json.dumps(curr_devices))
                redis_client.json().set("device_state", "." ,json.dumps(device_state))
        
            