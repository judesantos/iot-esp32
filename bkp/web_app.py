from app.oled import OLED 
from app import wifimgr

import machine
import time
import gc

oled = OLED.instance()

try:
  import usocket as socket
except:
  import socket

led = machine.Pin(2, machine.Pin.OUT)

try:
    oled.text("Init AP server...")
    wlan = wifimgr.get_connection()
    if wlan is None:
        oled.text("  Connect failed")
        oled.text("  EXIT!")
        while True:
            pass
except OSError as e:
    print('wifi manager error:\n')
    print(e)
    oled.text("   Exception!")
    while True:
        pass

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.

oled.reset()
oled.text("   ESP32 App")
oled.text("ip:" + wifimgr.device_server_ip)
oled.text("")
oled.text(" listening...")

def web_page():

  print('opening webpage') 

  gpio_state="OFF"
  if led.value() == 1:
    gpio_state="ON"
  
  f_html = open('./html/main.html', 'r')
  f_css = open('./css/styles.css', 'r')

  css = f_css.read()
  html = f_html.read()

  if None != html and None != css:
    css = "<style type='text/css'>" + str(css) + "</style>" 
    response = html.format(css_styles=css, gpio_state=gpio_state)
    return response
  else:
    return "Unknown Server Exception."  
  
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)

    print('Got a connection from %s' % str(addr))
    oled.textPosV("in:" + str(addr[0]), y=5)

    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)

    print('Content = %s' % request)

    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
      print('LED ON')
      oled.textPosV(' cmd: LED ON', y=6)
      led.value(1)
    if led_off == 6:
      print('LED OFF')
      oled.textPosV(' cmd: LED OFF', y=6)
      led.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

    time.sleep(3)
    oled.textPosV(" listening...", y=4)
    oled.text("")

  except OSError as e:
    conn.close()
    oled.text('Connection closed')
    print('Connection closed')
