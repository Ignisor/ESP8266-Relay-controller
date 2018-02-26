import time

from data.pins import RELAY
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


def process_get(request):
    content = HTML
    return Response(200, content)


def process_post(request):
    RELAY.value(ON)
    time.sleep(5)
    RELAY.value(OFF)
    return process_get(request)


views = {
    'POST': process_post,
    'GET': process_get,
}


s = Server(views)
s.activate_server()
