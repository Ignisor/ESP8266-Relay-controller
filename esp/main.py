from data.wifi import reset_if_not_connected
from data.pins import RELAY, ON, OFF, check_button
from server import server_app


def main_loop():
    is_connected = reset_if_not_connected()
    if is_connected:
        RELAY.value(ON)  # keep relay closed if wi-fi connection is ok
    else:
        RELAY.value(OFF)  # open relay and return false
        return False

    check_button()
    return True


server_app.activate_server(main_loop)
