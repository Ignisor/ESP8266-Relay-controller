# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import time

import gc
import webrepl

import wifi
from pins import LED


wifi.enable_wifi()
is_connected = wifi.connect()

LED.value(not is_connected)  # 'not' because 0 - is enable for led

webrepl.start()
gc.collect()
