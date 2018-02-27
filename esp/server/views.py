from utils.pins import open_relay
from . import server_app as srv
from .core import Response


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


@srv.view('GET', '/')
def process_get(request):
    content = HTML
    return Response(200, content)


@srv.view('POST', '/')
def process_post(request):
    open_relay()
    return process_get(request)