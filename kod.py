import socket
import network
from m5stack import *
from m5ui import *
from uiflow import *

setScreenColor(0x000000)
MAX_LEN = len("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
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
ans_l = ["0", "A", "B", "C", "D"]
answers = []
question = ""
curr_ans = ans_l[0]
curr_ans_i = 0
#Stage 2

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
  if curr_ans_i != 4:
    curr_ans_i = curr_ans_i + 1
    curr_ans = ans_l[curr_ans_i]
    render_question(curr_ans_i)

def render_question(j):
  global contents
  global answers
  global question
  global curr_ans
  global curr_ans_i
  send_message("rendering " + str(j))
  if j == 0:
    needed = len(question) // MAX_LEN
    rem = len(question) % MAX_LEN
    if rem != 0:
      needed = needed + 1
    
    for i in range(needed):
      if i == 0:
        contents[i].setText(question[:MAX_LEN])
      else:
        contents[i].setText(question[MAX_LEN * i:MAX_LEN * (i + 1)])
  else:
    needed = len(answers) // MAX_LEN
    rem = len(answers) % MAX_LEN
    if rem != 0:
      needed = needed + 1
    
    for i in range(needed):
      if i == 0:
        contents[i].setText(answers[j-1][:MAX_LEN])
      else:
        contents[i].setText(answers[j-1][MAX_LEN * i:MAX_LEN * (i + 1)])
  show_content()
      

def hide_content():
  global contents
  for i in range(11):
    contents[i].hide()
def show_content():
  global contents
  for i in range(11):
    contents[i].show()

stage = 0
shown = 0
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
      data = "question:;:What is the capital of France?What is the capital of France?What is the capital of France?What is the capital of France?What is the capital of France?What is the capital of France?What is the capital of France?;Paris;London;Berlin;Madrid"   
      #recieve_message_server()
      handle_data(data)
      send_message(question)
      for i in answers:
        send_message(i)
      

  if stage == 2 and shown == 1:
      btnA.wasPressed(prev_page)
      btnC.wasPressed(next_page)
      shown = 2
      info.hide()
      render_question(0)
      
      #btnB.wasPressed(confirm_answer)
      

  wait_ms(5)
  