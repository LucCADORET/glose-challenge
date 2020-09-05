class HTTPRequest():
    """
    This class is used to parse a raw HTTP request, and extract the method, headers, uri etc.
    It's not complete, but can be filled-in for extended purposes
    """

    def __init__(self, request_string):
        lines = request_string.split('\r\n')
        method_line = lines[0]
        method_line_split = method_line.split(' ')
        self.method = method_line_split[0]
        self.uri = method_line_split[1]
