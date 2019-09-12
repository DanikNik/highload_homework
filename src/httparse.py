RESPONSE_VERBOSE_ANSWERS = {
    200: "OK",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
}


class Request:
    def __init__(self):
        self.method = ""
        self.path = ""
        self.protocol = ""
        self.headers = {}
        self.query_arguments = {}

    def parse(self, data: str):
        try:
            init_line, _, other = data.partition('\r\n')
            self.method, query_string, self.protocol = init_line.split(' ')

            try:
                self.path, query_args = query_string.split('?')
                self.query_arguments = dict(
                    map(
                        lambda x: x.split('='),
                        query_args.split('&')
                    )
                )
            except ValueError:
                self.path = query_string

            self.headers = dict(
                map(
                    lambda x: x.split(": "),
                    other.partition('\r\n\r\n')[0].strip('\r\n ').split("\r\n")
                )
            )
            return
        except ValueError:
            pass


class Response:
    def __init__(self,
                 protocol: str = "HTTP/1.1",
                 status: int = 200,
                 headers: dict = None,
                 data: bytes = b""):
        if headers is None:
            headers = {}
        self.protocol = protocol
        self.status = status
        self.headers = headers
        self.data = data

    def __str__(self) -> str:
        return self.headers_to_string()

    def headers_to_string(self) -> str:
        init_line = ' '.join([self.protocol, str(self.status), RESPONSE_VERBOSE_ANSWERS[self.status]])
        headerlines = '\r\n'.join(
            list(map(lambda x: ': '.join(list(map(str, x))), zip(self.headers.keys(), self.headers.values()))))
        return "{}\r\n{}\r\n\r\n".format(init_line, headerlines)
