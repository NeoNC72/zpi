import socket
import network
from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x000000)
MAX_LEN = len("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
UDP_IP = "192.168.244.15"
UDP_PORT = 558
addr = (UDP_IP, UDP_PORT)

udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsocket.connect(addr)

def send_message(message):
  global udpsocket
  udpsocket.send(message)

def receive_message():
  global udpsocket
  data = udpsocket.recv(1024)
  return data.decode()

send_message("get_ip:;:0")
ip = receive_message()
MY_IP = ip
MY_PORT = 559
MY_ADDR = (MY_IP, MY_PORT)
udpsocketserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsocketserver.bind(MY_ADDR)

def recieve_message_server():
  global udpsocketserver
  data = udpsocketserver.recv(1024)
  return data.decode()

id_n = 1

def id_minus():
  global id_n
  global id_l
  global id_err
  id_err.hide()
  id_err.setText("X")
  if id_n > 1:
    id_n = id_n - 1
    id_l.setText(str(id_n))
  if id_n > 9:
    id_l.setPosition(114, 84)
  else:
    id_l.setPosition(137, 84)
  pass

def nothing():
  pass

def id_plus():
  global id_n
  global id_l
  id_err.hide()
  id_err.setText("X")
  if id_n < 9999:
    id_n = id_n + 1
    id_l.setText(str(id_n))
  if id_n > 9:
    id_l.setPosition(114, 84)
  else:
    id_l.setPosition(137, 84)
  pass

def id_ok():
  global id_n
  global stage
  global id_l
  global plus
  global minus
  global ok
  global rendered
  global id_err
  test = check_valid_id()
  if test == True:

    stage = 1
    id_l.hide()
    plus.hide()
    minus.hide()
    ok.hide()
  else:
    id_err.setText(check_valid_id())
    id_err.show()
    

def check_valid_id():
  global id_n
  send_message("register_id:;:" + str(id_n))
  response = receive_message()
  if response == "valid":
    return True
  else:
    return response

def handle_data(data):
  global stage
  global question
  global answers
  if ":" in data:
    s_data = data.split(":;:")
    type_d = s_data[0]
    content = s_data[1]
  else:
    type_d = data
  if type_d == "alive":
    send_message("alive")
  if type_d == "question":
    data_q = content.split(";")
    question = data_q[0]
    answers = data_q[1:]
    stage = 2
    send_message("ok")
def prev_page():
  global curr_ans_i
  global curr_ans
  
  if curr_ans_i != 0:
    curr_ans_i = curr_ans_i - 1
    curr_ans = ans_l[curr_ans_i]
    render_question(curr_ans_i)

def next_page():
  global curr_ans_i
  global curr_ans
  if curr_ans_i != 3:
    curr_ans_i = curr_ans_i + 1
    curr_ans = ans_l[curr_ans_i]
    render_question(curr_ans_i)

def confirm_answer():
    global curr_ans_i
    global curr_ans
    global stage
    send_message("answer:;:" + str(id_n) + ";" + curr_ans)
    stage = 3
    state.setTitle('ID: ' + str(id_n) + "                    Answered")
    hide_content()
    null_content()



def data_to_lines(data):
    split_data = data.split()
    lines = []
    temp_line = ""
    temp_temp_line = ""
    if len(data) < MAX_LEN:
        return [data]

    for i in range(len(split_data)):
        temp_temp_line += split_data[i] + " "
        if len(temp_line) > MAX_LEN:
            lines.append(temp_line)
            temp_line = ""
            temp_temp_line = "" 

        else:
            temp_line = temp_temp_line
    lines.append(temp_line)
    return lines


def render_question(j):
  global contents
  global answers
  global question
  global curr_ans
  global curr_ans_i
  global state
  null_content()
  if j == 0:
    lines = data_to_lines(question)
    for i, line in enumerate(lines):
      contents[i].setText(line)
  else:
    lines = data_to_lines(answers[j - 1])
    for i, line in enumerate(lines):
      contents[i].setText(line)

  show_content()
  state.setTitle('ID: ' + str(id_n) + "                            " + curr_ans)

      

def hide_content():
  global contents
  for i in range(11):
    contents[i].hide()

def show_content():
  global contents
  for i in range(11):
    contents[i].show()

def null_content(from_i = 0, to_i = 11):
  global contents
  for i in range(from_i, to_i):
    contents[i].setText(" ")


def get_status():
  return "1/2"
  """
  send_message("status")
  return receive_message()"""

def show_results():
    global contents
    global state
    global results
    global res_parsed
    global res_count
    null_content()
    btnB.wasPressed(nothing)
    btnC.wasPressed(next_page_results)
    btnA.wasPressed(prev_page_results)
    tmp_list = []
    for i in range(1, len(results)):
        tmp_list.append(results[i])
        if len(tmp_list) == 9:
          res_parsed.append(tmp_list)
          tmp_list = []
          res_count += 1
  
    
    contents[0].setText("Correct answer: " + results[0] + "  Your answer: " + curr_ans)
    contents[1].setText("Rank: ID ............ Time")
    render_results(0)
    show_content()
       
def render_results(i):
    global contents
    global res_parsed
    null_content(2,11)
    wait_ms(100)
    for j, l in enumerate(res_parsed[i]):
      contents[j + 2].setText(l)



def next_page_results():
    global curr_res
    global res_count
    
    if curr_res == res_count:
        return
    
    curr_res = curr_res + 1
    
    render_results(curr_res)
 

def prev_page_results():
    global curr_res
    global res_count
    
    if curr_res == 0:
      return
    curr_res = curr_res - 1
    render_results(curr_res)

#Stage 0
id_l = M5TextBox(137, 84, "1", lcd.FONT_DejaVu72, 0xFFFFFF, rotate=0)
plus = M5TextBox(224, 198, "+", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)
minus = M5TextBox(58, 198, "-", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)
ok = M5TextBox(138, 206, "ok", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)
id_err = M5TextBox(55, 28, "X", lcd.FONT_DejaVu24, 0xff0000, rotate=0)

id_l.hide()
plus.hide()
minus.hide()
ok.hide()
id_err.hide()
#Stage 0

#Stage 1
state = M5Title(title="ID: ", x=3, fgcolor=0xFFFFFF, bgcolor=0x090909)
info = M5TextBox(34, 106, "No question", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)

state.hide()
info.hide()
#Stage 1
#Stage 2
contents = []
for i in range(11):
  contents.append(M5TextBox(0, 30 + i * 20, " ", lcd.FONT_Default, 0xFFFFFF, rotate=0))
ans_l = ["Q", "A", "B", "C"]
answers = []
question = ""
curr_ans = ans_l[0]
curr_ans_i = 0
#Stage 2

#Stage 3
ans = M5TextBox(29, 68, "Answered: ", lcd.FONT_DejaVu40, 0xFFFFFF, rotate=0)
user_info = M5TextBox(10, 109, "Waiting for other devices to answer", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
count_dev = M5TextBox(112, 149, "/", lcd.FONT_DejaVu56, 0xFFFFFF, rotate=0)
status_label = M5TextBox(35, 167, "Status:", lcd.FONT_Ubuntu, 0xFFFFFF, rotate=0)
ans.hide()
user_info.hide()
count_dev.hide()
status_label.hide()
#Stage 3
#Stage 4
res_parsed = []
res_count = 0
curr_res = 0
#Stage 4
stage = 0
shown = 0
showing = False

while True:
    if stage == 0:
        id_l.show()
        plus.show()
        minus.show()
        ok.show()
        
        btnA.wasPressed(id_minus) # type: ignore
        btnC.wasPressed(id_plus)
        btnB.wasPressed(id_ok)

    if stage == 1 and shown == 0:
        btnA.wasPressed(nothing)
        btnC.wasPressed(nothing)
        btnB.wasPressed(nothing)
        shown = 1
        state.show()
        info.show()
        state.setTitle('ID: ' + str(id_n) + "                      Waiting...")
        data = "question:;:What is the capital of France?capital of France?What is the capital of France?;Paris;London;Berlin;Madrid"   
        #recieve_message_server()
        handle_data(data)
        send_message(question)
        for i in answers:
            send_message(i)
        

    if stage == 2 and shown == 1:
        btnA.wasPressed(prev_page)
        btnC.wasPressed(next_page)
        btnB.wasPressed(confirm_answer)
        shown = 2
        info.hide()
        render_question(0)

    if stage == 3 and shown == 2:
        shown = 3
        ans.setText("Answered: " + curr_ans)
        ans.show()
        user_info.show()
        status_ans = "done"
        if status_ans == "done":
            stage = 4
            wait_ms(1000)
            ans.hide()
            user_info.hide()
            count_dev.hide()
            status_label.hide()
        else:
            count_dev.setText(status_ans)
            count_dev.show()
            status_label.show()
    if stage == 4 and shown == 3:
      shown = 4
      state.setTitle('ID: ' + str(id_n) + "                    Results")
      if not showing:
        results = "A; 1.: 7 ............ 1:13; 2.: 9 ............1:15; 3.: 10 ............1:17; 4.: 11 ............1:19; 5.: 12 ............1:21; 6.: 13 ............1:23; 7.: 14 ............1:25; 8.: 15 ............1:27; 9.: 16 ............1:29; 10.: 17 ............1:31; 11.: 18 ............1:33; 12.: 19 ............1:35; 13.: 20 ............1:37; 14.: 21 ............1:39; 15.: 22 ............1:41; 16.: 23 ............1:43; 17.: 24 ............1:45; 18.: 25 ............1:47; 19.: 26 ............1:49; 20.: 27 ............1:51; 21.: 28 ............1:53; 22.: 29 ............1:55; 23.: 30 ............1:57; 24.: 31 ............1:59; 25.: 32 ............2:01; 26.: 33 ............2:03; 27.: 34 ............2:05; 28.: 35 ............2:07; 29.: 36 ............2:09; 30.: 37 ............2:11; 31.: 38 ............2:13; 32.: 39 ............2:15; 33.: 40 ............2:17; 34.: 41 ............2:19; 35.: 42 ............2:21; 36.: 43 ............2:23; 37.: 44 ............2:25; 38.: 45 ............2:27; 39.: 46 ............2:29; 40.: 47 ............2:31; 41.: 48 ............2:33; 42.: 49 ............2:35; 43.: 50 ............2:37; 44.: 51 ............2:39; 45.: 52 ............2:41; 46.: 53 ............2:43; 47.: 54 ............2:45"
        results = results.split(";")
        show_results()
        showing = True

      

    wait_ms(5)
  