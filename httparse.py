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
        self.is_binary = False

    def __str__(self):
        return self.to_string()

    def to_string(self):
        init_line = ' '.join([self.protocol, str(self.status), RESPONSE_VERBOSE_ANSWERS[self.status]])
        headerlines = '\r\n'.join(
            list(map(lambda x: ': '.join(list(map(str, x))), zip(self.headers.keys(), self.headers.values()))))
        # if not self.is_binary:
        #     return "{}\r\n{}\r\n\r\n{}".format(init_line, headerlines, self.data)
        # else:
        return "{}\r\n{}\r\n\r\n".format(init_line, headerlines)


if __name__ == "__main__":
    package = '''GET /docs/index.html HTTP/1.1\r
Host: www.nowhere123.com\r
Accept: image/gif, image/jpeg, */*\r
Accept-Language: en-us\r
Accept-Encoding: gzip, deflate\r
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r
\r\n'''

    pack = "GET / HTTP/1.1\r\n"

    req = Request()
    req.parse(package)
    # resp = Response()
    # resp.status = 200
    # resp.protocol = "HTTP/1.1"
    # resp.headers = {
    #     "Content-Length": "44",
    #     "Content-Type": "text/html"
    # }
    # resp.data = "SOME CHUNK"
    # al = str(resp)
    # print(al)
    pass
