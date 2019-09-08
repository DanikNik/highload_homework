status_ok = 200
status_notfound = 404
status_forbidden = 403
status_method_not_allowed = 405
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

    def __eq__(self, other):
        return self.method == other.method and \
               self.path == other.path and \
               self.protocol == other.protocol and \
               self.headers == other.headers

    def __ne__(self, other):
        return not (self == other)

    def parse(self, data: str):
        init_line, _, other = data.partition('\n')
        self.method, self.path, self.protocol = init_line.split(' ')
        self.headers = dict(
            map(
                lambda x: x.split(": "),
                other.partition('\r\n')[0].strip('\n ').split("\n")
            )
        )


class Response:
    def __init__(self):
        self.protocol = ""
        self.status: int = 0
        self.headers = {}
        self.data = ""

    def __str__(self):
        init_line = ' '.join([self.protocol, str(self.status), RESPONSE_VERBOSE_ANSWERS[self.status]])
        headerlines = '\n'.join(
            list(map(lambda x: ': '.join(list(map(str, x))), zip(self.headers.keys(), self.headers.values()))))
        return "{}\n{}\n\r\n{}".format(init_line, headerlines, self.data)
        pass


if __name__ == "__main__":
    package = '''GET /docs/index.html HTTP/1.1
Host: www.nowhere123.com
Accept: image/gif, image/jpeg, */*
Accept-Language: en-us
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
\r\n'''

    req = Request()
    req.parse(package)
    resp = Response()
    resp.status = 200
    resp.protocol = "HTTP/1.1"
    resp.headers = {
        "Content-Length": "44",
        "Content-Type": "text/html"
    }
    resp.data = "helalwfhia;owf;aowh;foawh;'oifhaw;oifh;oawih;foiahw;oifhaw;oifh;aowih;foiawh;foiawh;oifhaw;iofh;awiohf;oawih;foiawh;foiahw;oihlo there"
    al = str(resp)
    print(al)
    pass
