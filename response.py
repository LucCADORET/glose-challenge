class HTTPResponse():
    STATUS_CODES = {
        200: 'OK',
        404: 'Not Found',
    }
    HEADERS = {
        'Server': 'GloseChal',
        'Content-Type': 'text/html',
    }

    def __init__(self, code, body):
        self.code = code
        self.body = body

    def raw_response(self):
        """Returns the full raw http response, encoded"""
        status_string = self.get_status_string(status_code=self.code)
        headers_string = self.get_headers_string()
        return "{}{}\r\n{}".format(
            status_string,
            headers_string,
            self.body
        ).encode()

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
