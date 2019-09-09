import unittest
from httparse import Request, Response


class RequestTests(unittest.TestCase):
    def test_request_parse(self):
        package = '''GET /docs/index.html HTTP/1.1\r
Host: www.nowhere123.com\r
Accept: image/gif, image/jpeg, */*\r
Accept-Language: en-us\r
Accept-Encoding: gzip, deflate\r
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r
\r\n'''

        test_req = Request()
        test_req.parse(package)

        equal_req = Request()
        equal_req.method = "GET"
        equal_req.path = "/docs/index.html"
        equal_req.protocol = "HTTP/1.1"
        equal_req.headers = {
            "Host": "www.nowhere123.com",
            "Accept": "image/gif, image/jpeg, */*",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        }
        self.assertEqual(test_req.method, equal_req.method)
        self.assertEqual(test_req.path, equal_req.path)
        self.assertEqual(test_req.protocol, equal_req.protocol)
        self.assertEqual(test_req.headers, equal_req.headers)


class ResponseTests(unittest.TestCase):
    def test_response_to_string(self):
        equal_resp_text = """HTTP/1.1 200 OK\r
Server: Apache/2.2.14 (Win32)\r
ETag: "10000000565a5-2c-3e94b66c2e680"\r
Accept-Ranges: bytes\r
Content-Length: 44\r
Connection: close\r
Content-Type: text/html\r
\r
<html><body><h1>It works!</h1></body></html>"""
        test_resp = Response()
        test_resp.protocol = "HTTP/1.1"
        test_resp.status = 200
        test_resp.headers = {
            'Server': 'Apache/2.2.14 (Win32)',
            'ETag': '"10000000565a5-2c-3e94b66c2e680"',
            'Accept-Ranges': 'bytes',
            'Content-Length': '44',
            'Connection': 'close',
            'Content-Type': 'text/html',
        }
        test_resp.data = "<html><body><h1>It works!</h1></body></html>"
        self.assertEqual(test_resp.to_string(), equal_resp_text)


if __name__ == '__main__':
    unittest.main()
