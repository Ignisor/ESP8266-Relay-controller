from data import conf
from utils.pins import open_relay
from . import server_app as srv
from .core import Response, TemplateResponse


@srv.view('GET', '/')
def process_get(request):
    template = "index.html"
    return TemplateResponse(200, template)


@srv.view('POST', '/')
def process_post(request):
    open_relay()
    return process_get(request)


@srv.view('GET', '/error/')
def error_view(request):
    with open(conf.ERROR_LOG_FILENAME) as err_file:
        return Response(200, err_file.read())
