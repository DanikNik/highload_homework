from httparse import Request, Response
from datetime import datetime
from pytz import timezone
import os

DOCUMENT_ROOT = "/home/daniknik/http-test-suite"


def handle_request(req: Request):
    if req.method == "HEAD":
        return make_response(req, False)
    elif req.method == "GET":
        return make_response(req, True)
    else:
        return Response(status=405)
    pass


def get_time_now_http():
    return timezone('Europe/Moscow').localize(datetime.now()).strftime("%a, %d %b %Y %H:%M:%S %Z")


def make_response(req: Request, put_data: bool):
    resp = Response(headers={
        "Server": "py_nginx",
        "Date": get_time_now_http()
    })
    print(req.path)

    filepath = os.path.join(DOCUMENT_ROOT, req.path)
    print(filepath)

    return resp


def read_file(filename: str):
    pass


if __name__ == "__main__":
    path = "/httptest"
    print(path.split('/'))
