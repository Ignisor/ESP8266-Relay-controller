import socket
import gc


CODE_HEADERS = {
    200: 'OK',
    400: 'Bad Request',
    404: 'Not Found',
    500: 'Internal Server Error',
}


class Server(object):
    """ Class describing a simple HTTP server"""
    def __init__(self, views, port=80):
        self.host = ''  # works on all avaivable network interfaces
        self.views = views
        self.port = port

        self.socket = None

    def activate_server(self):
        """ Attempts to aquire the socket and launch the server """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self._wait_for_connections()

    def shutdown(self):
        """ Shut down the server """
        self.socket.shutdown(socket.SHUT_RDWR)

    def _wait_for_connections(self):
        """ Main loop awaiting connections """
        self.socket.listen(3)  # maximum number of queued connections

        while True:
            conn, addr = self.socket.accept()

            data = bytes()
            while True:
                d = conn.recv(128)  # receive data from client
                data += d
                if d.endswith(b'\r\n\r\n'):
                    break

            data_str = bytes.decode(data)  # decode it to string

            request = Request(data_str, addr)

            if request.method in self.views.keys():
                view = self.views.get(request.method, lambda r: Response(404))
            else:
                view = lambda r: Response(400)

            response = view(request)

            server_response = response.encode()

            conn.send(server_response)
            conn.close()

            gc.collect()


class Request(object):
    def __init__(self, data, addr):
        if type(data) == str:
            self.body = data
        else:
            self.body = bytes.decode(data)

        self.address = addr
        self.method = self.body.split(' ')[0]


class Response(object):
    def __init__(self, code, content=None):
        self.code = code
        self.content = content
        self.headers = self._gen_headers()

    def _gen_headers(self):
        """ Generates HTTP response Headers. Ommits the first line! """
        # determine response code
        code_h = CODE_HEADERS[self.code]
        h = 'HTTP/1.1 {code} {text}\n'.format(code=self.code, text=code_h)

        # write further headers
        h += 'Content-type: text/html\n'
        h += 'Server: ESP-Python-HTTP-Server\n'
        h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

        return h

    def encode(self):
        resp = self.headers.encode()
        if self.content:
            resp += self.content.encode()

        return resp
