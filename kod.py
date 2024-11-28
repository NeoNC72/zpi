
import module
lan = module.get(module.LANBASE)

setScreenColor(0x000000)




id_n = 1

def id_minus():
  global id_n
  global id_l
  global id_err
  id_err.hide()
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
  req = lan.http_request(method='POST', url='http://sulis15.zcu.cz:5005/register_id',json={'id':id_n}, headers={})
  if req.text == 'OK':
    return True
  else:
    return req.text



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


stage = 0
while True:
  if stage == 0:
      id_l.show()
      plus.show()
      minus.show()
      ok.show()
      
      btnA.wasPressed(id_minus) # type: ignore
      btnC.wasPressed(id_plus)
      btnB.wasPressed(id_ok)

  if stage == 1:
      id_l.show()
      btnA.wasPressed(nothing)
      btnC.wasPressed(nothing)
      btnB.wasPressed(nothing)

  wait_ms(5)