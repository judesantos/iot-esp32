
try:
    import usocket as socket
except:
    import socket

from app.oled import OLED
import network
import time
import gc

global network_ip

gc.collect()
gc.mem_free()

oled = OLED.instance()

SSID = 'santos404'
PASSWORD = '74birun@m@x11'

station = network.WLAN(network.STA_IF)

oled.text("     WIFI")
oled.text("")
oled.text("ssid: " + SSID)
oled.text("")
oled.text("connecting...")
print("connecting to wifi...")

station.active(True)
station.connect(SSID, PASSWORD)

for retry in range(15):
    connected = station.isconnected()
    if connected:
        break
    time.sleep(0.5)
    print('.', end='')
if connected:
    oled.text("connect OK!")
    print("connection successful!")
    ips = station.ifconfig()
    network_ip = ips[0]
    print('\nNetwork config: ', ips)
else:
    oled.text("connect failed!")
    print('\nFailed. Not Connected to: ' + SSID)

