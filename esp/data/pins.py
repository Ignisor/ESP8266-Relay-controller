import machine


LED = machine.Pin(2, machine.Pin.OUT)
BUTTON = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)  # D2 pin
RELAY = machine.Pin(14, machine.Pin.OUT)  # D5 pin
RELAY.value(1)
