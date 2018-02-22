# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import time

import gc
import machine
import webrepl
import network

import conf

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)
ap_if.active(False)
sta_if.active(True)

led = machine.Pin(2, machine.Pin.OUT)

for i in range(conf.CONNECT_RETRIES):
    t_start = time.time()
    sta_if.connect(conf.SSID, conf.PASSWORD)

    while not sta_if.isconnected():
        led.value(0)  # 0 - is enable for led
        time.sleep(0.1)
        led.value(1)

        t = time.time() - t_start
        if t > conf.CONNECTION_TIME:
            break

    if sta_if.isconnected():
        break

led.value(not sta_if.isconnected())  # 'not' because 0 - is enable for led

webrepl.start()
gc.collect()
