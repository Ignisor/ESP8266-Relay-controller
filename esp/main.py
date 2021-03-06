import sys
import machine

from data import conf
from utils.wifi import reset_if_not_connected
from utils.pins import RELAY, ON, OFF, check_button
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


try:
    server_app.activate_server(main_loop)
except Exception as e:
    # write exception to file and restart a machine in case of error
    with open(conf.ERROR_LOG_FILENAME, 'w') as err_file:
        sys.print_exception(e, err_file)
    machine.reset()
