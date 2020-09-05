import socket
import logging
import sys
from request import HTTPRequest
import os

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class HTTPServer:
    host = '127.0.0.1'
    HEADERS = {
        'Server': 'GloseChal',
        'Content-Type': 'text/html',
    }
    STATUS_CODES = {
        200: 'OK',
        404: 'Not Found',
    }

    def __init__(self, port=4321, root_dir='/home/luc/Documents/glose-challenge/public'):
        self.port = port
        self.root_dir = root_dir

    def start(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(5)

        logger.info("HTTP Server started on {}".format(
            serversocket.getsockname()))

        while True:
            conn, addr = serversocket.accept()
            data = conn.recv(1024)

            request = HTTPRequest(data.decode())
            logger.debug("{}:{} => {} {}".format(addr[0], addr[1], request.method, request.uri))

            response = self.handle_request(request)

            conn.sendall(response.encode())
            conn.close()

    def handle_request(self, request):
        """
        Build up the proper http response depending on the request:
            - status line
            - headers
            - body
        """

        status_string = self.get_status_string(status_code=200)
        headers_string = self.get_headers_string()
        body_string = self.get_body_string(request)

        return "{}{}\r\n{}".format(
            status_string,
            headers_string,
            body_string
        )

    def get_body_string(self, request):
        """Returns the proper body string, depending on the client's request"""
        uri = request.uri

        # Try to find the resource in the root dir content
        path = os.path.join(self.root_dir)

        return "<h1>Salut</h1>"

    def get_status_string(self, status_code):
        """Returns the HTTP status code line"""
        reason = self.STATUS_CODES[status_code]
        return "HTTP/1.1 {} {}\r\n".format(status_code, reason)

    def get_headers_string(self):
        """Returns a string containing the headers of the response"""
        headers = ""
        for h in self.HEADERS:
            headers += "{}: {}\r\n".format(h, self.HEADERS[h])
        return headers

