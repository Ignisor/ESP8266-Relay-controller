import time

import machine

from data import conf

led = machine.Pin(2, machine.Pin.OUT)

t_start = time.time()
while True:
    led.value(0)  # 0 - is enable for led
    time.sleep(0.1)
    led.value(1)
    time.sleep(0.1)

    t = time.time() - t_start
    if t >= conf.CONNECTION_TIME:
        print(t)
        break
