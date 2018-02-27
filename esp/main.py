import time

from data.wifi import reset_if_not_connected
from data.pins import RELAY, BUTTON
from server.core import Server, Response


ON = 0
OFF = 1

HTML = """\
<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>ESP-Door</title>
 </head>
 <body>

 <form action="." method="POST">
  <p><input type="submit" value="Open"></p>
 </form>

 </body>
</html>
"""


def open_relay():
    print('Opening door...')
    RELAY.value(ON)
    time.sleep(5)
    RELAY.value(OFF)

    return True


def process_get(request):
    content = HTML
    return Response(200, content)


def process_post(request):
    open_relay()
    return process_get(request)


def check_button():
    if BUTTON.value() == ON:
        open_relay()


def main_loop():
    is_connected = reset_if_not_connected()
    if is_connected:
        RELAY.value(OFF)  # keep door closed if wi-fi connection is ok
    else:
        RELAY.value(ON)
        return False

    check_button()
    return True


views = {
    'POST': process_post,
    'GET': process_get,
}

s = Server(views)
s.activate_server(main_loop)
