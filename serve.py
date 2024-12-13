from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import time
import redis

app = Flask(__name__)

# Global variable to store the text
display_text = "Default Text"

UDP_IP = "192.168.244.15"
UDP_PORT = 1470

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

# Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def check_redis_for_updates():
    global display_text
    last_text = None
    while True:
        new_text = redis_client.get('results')
        if new_text and new_text != last_text:
            tmp = ""
            print(f"New text: {new_text}")
            last_text = new_text
            new_text = (new_text.decode('utf-8')).split(";")
            tmp += f"Správná odpověd byla: {new_text[0]}<br>"
            for i in range(1, len(new_text)):
                tmp += f"{new_text[i].replace('X', '..............')}<br>"
            
            
            display_text = tmp            
            
            
        time.sleep(5)  # Check every 5 seconds

@app.route('/', methods=['GET', 'POST'])
def index():
    global display_text
    if request.method == 'POST':
        # Handle form submission
        input1 = request.form.get('Q')
        input2 = request.form.get('A_A')
        input3 = request.form.get('A_B')
        input4 = request.form.get('A_C')
        radio2 = request.form.get('correct_answer')
        inputc = request.form.get('CS')
        
        # You can process the inputs and radio selections here
        display_text = f"Received: {input1}, {input2}, {input3}, {input4}, {radio2}, {inputc}"
        ans = ""
        if radio2 is not None:
            ans = radio2
        
        build_cmd = f"new_question:;:{input1}:;:{ans}:;:{inputc}:;:{input2}:;:{input3}:;:{input4}"
        sock.sendto(build_cmd.encode(), ("192.168.244.15", 558))
        
        return redirect(url_for('index'))
    return render_template('index.html', display_text=display_text)

@app.route('/update_text', methods=['POST'])
def update_text():
    global display_text
    display_text = request.form.get('new_text')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Start the background thread to check Redis for updates
    threading.Thread(target=check_redis_for_updates, daemon=True).start()
    app.run(debug=True)