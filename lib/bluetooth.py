
import utime
import bluetooth

bt = bluetooth.Bluetooth()

bt.active(True)
bt.advertise(1000, 'yourtechy-bt')


