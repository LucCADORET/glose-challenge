import socket
import logging
import sys
from request import HTTPRequest
from response import HTTPResponse
import os
import asyncio

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

    def __init__(self, port=4321, root_dir='/home/luc/Documents/glose-challenge/public'):
        self.port = port
        self.root_path = os.path.abspath(root_dir)

    def start(self):
        asyncio.run(self.server())

    async def server(self):
        server = await asyncio.start_server(self.poll, self.host, self.port)
        logger.info(
            "Starting server at http://{}:{}".format(self.host, self.port))
        logger.info("Serving dir: {}".format(self.root_path))
        await server.serve_forever()

    async def poll(self, reader, writer):
        while True:
            data = await reader.read(1024)  # Max number of bytes to read
            if not data:
                break
            request = HTTPRequest(data.decode())
            raw_response = self.handle_request(request)
            logger.debug("{} {} {}".format(
                request.method, request.uri, len(raw_response)))
            writer.write(raw_response)
            await writer.drain()
        writer.close()

    def handle_request(self, request):
        """
        Build up the proper http response depending on the request:
            - status line
            - headers
            - body
        """

        body_string = None
        try:
            body_string = self.get_body_string(request)
        except:
            pass  # We could handle different type of errors here obviously

        # Our handling is very simple and only handles 200 (OK) and 404 (Not Found)
        if body_string:
            response = HTTPResponse(200, body_string)
        else:
            response = HTTPResponse(404, "404 Not Found")
        return response.raw_response()

    def get_body_string(self, request):
        """Returns the proper body string, depending on the client's request"""
        uri = request.uri

        # Try to find the resource in the root dir content
        path = os.path.normpath(self.root_path + uri)

        # If it's a directory: we'll return a nice listing of the content of that dir
        if os.path.isdir(path):
            return self.get_dir_string(path)

        # If it's a file, we'll simply return the file content as string (we'll assume it's compatible)
        elif os.path.isfile(path):
            f = open(path, "r")
            return f.read()

        # Else consider that it's not found
        raise Exception("Not Found")

    def get_dir_string(self, path):
        """ Build a nice string for the page to be show to the user when he requests a directory """
        list_dir = os.listdir(path)
        response_string = ''

        # Add the previous link
        if path != self.root_path:
            response_string += '<a href="..">..</a><br><br>\r\n'
        for content in list_dir:
            content_path = os.path.join(path, content)
            prefix = ""
            if os.path.isdir(content_path):
                prefix = "[DIR] "
            content_relative_path = os.path.relpath(content_path, self.root_path)
            response_string += '<a href="{}">{}</a><br>\r\n'.format(
                content_relative_path, "{}{}".format(prefix, content))
        return response_string
