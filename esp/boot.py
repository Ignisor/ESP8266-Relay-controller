from data import wifi
from data.pins import LED


wifi.enable_wifi()
is_connected = wifi.connect()

LED.value(not is_connected)  # 'not' because 0 - is enable for led
