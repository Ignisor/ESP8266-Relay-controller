import socket
from uerrno import EAGAIN, ETIMEDOUT
import gc

from data import conf

CODE_HEADERS = {
    200: 'OK',
    400: 'Bad Request',
    404: 'Not Found',
    500: 'Internal Server Error',
}


class Server(object):
    """ Class describing a simple HTTP server"""
    def __init__(self, port=80):
        self.host = ''  # works on all avaivable network interfaces
        self.views = {}
        self.port = port

        self.socket = None

    def activate_server(self, main_task):
        """ Attempts to aquire the socket and launch the server """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self._wait_for_connections(main_task)

    def view(self, method, url):
        """View decorator"""
        def view_decorator(func):
            def func_wrapper(request):
                try:
                    return func(request)
                except Exception:
                    return Response(500, "500 Server Error")

            key = '{}:{}'.format(method.lower(), url.lower())
            self.views[key] = func_wrapper

            return func_wrapper
        return view_decorator

    def _wait_for_connections(self, main_task):
        """
        Main non blocking loop awaiting connections
        :param main_task: function to call in loop while waiting for connection
        """
        self.socket.listen(3)
        self.socket.setblocking(False)

        while True:
            if not main_task():
                break  # break the loop if main_tesk returned false

            s_data = dict(d.split('=') for d in str(self.socket).replace('>', '').split()[1:])

            if s_data.get('incoming', '0') != '0':
                try:
                    self._handle_connection()
                except OSError as e:
                    if e.args[0] != ETIMEDOUT:
                        raise e

                gc.collect()

    def _handle_connection(self):
        conn, addr = self.socket.accept()
        conn.settimeout(0.5)

        while True:
            try:
                data = self._get_data(conn)
                break
            except OSError as e:
                if e.args[0] != EAGAIN:
                    raise e

        data_str = bytes.decode(data)  # decode it to string
        request = Request(data_str, addr)

        view = self._get_view(request)
        response = view(request)
        server_response = response.encode()

        conn.send(server_response)
        conn.close()

    def _get_data(self, connection, chunk_size=128):
        data = b''
        while True:
            chunk = connection.recv(chunk_size)
            data += chunk
            if chunk.endswith(b'\r\n\r\n'):
                return data

    def _get_view(self, request):
        key = '{}:{}'.format(request.method.lower(), request.url.lower())
        return self.views.get(key, lambda r: Response(404))


class Request(object):
    def __init__(self, data, addr):
        if type(data) == str:
            self.body = data
        else:
            self.body = bytes.decode(data)

        self.address = addr
        self.method = self.body.split(' ')[0]
        self.url = self.body.split(' ')[1]


class Response(object):
    def __init__(self, code, content=None):
        self.code = code
        self.content = content
        self.headers = self._process_headers()

    def _gen_headers(self):
        """ Generates HTTP response Headers. Ommits the first line! """
        headers = []
        code_h = CODE_HEADERS[self.code]
        headers.append('HTTP/1.1 {code} {text}'.format(code=self.code, text=code_h))

        headers.append('Server: ESP-Python-HTTP-Server')
        headers.append('Connection: close')  # signal that the conection wil be closed after complting the request

        return headers

    def _process_headers(self):
        h = '\n'.join(self._gen_headers())
        h += '\n\n'
        return h

    def encode(self):
        resp = self.headers.encode()
        if self.content:
            resp += self.content.encode()

        return resp


class HTMLResponse(Response):
    def _gen_headers(self):
        headers = super()._gen_headers()
        headers.append('Content-type: text/html')

        return headers


class TemplateResponse(HTMLResponse):
    """Simple template render and response"""
    def __init__(self, code, template, context=None):
        self.template = TemplateResponse.render_template(template, context)

        super().__init__(code, self.template)

    @staticmethod
    def render_template(template_name, context=None):
        template = TemplateResponse.open_template(template_name)

        if context:
            template.format(**context)

        return template

    @staticmethod
    def open_template(template_name):
        path = conf.TEMPLATE_FOLDER
        path += template_name

        template = open(path, 'r').read()

        return template

