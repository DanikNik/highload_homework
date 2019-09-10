import urllib

from httparse import Request, Response
from datetime import datetime
from pytz import timezone
from pathlib import Path

import os

DOCUMENT_ROOT = "/home/daniknik/http-test-suite"
MIME_TYPES = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "swf": "application/x-shockwave-flash",
}


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

    filepath = os.path.join(DOCUMENT_ROOT, req.path.lstrip('/'))
    filepath = urllib.parse.unquote(filepath)
    aware_dir_enum = False
    if filepath[-1] == '/':
        filepath = os.path.join(filepath, "index.html")
        aware_dir_enum = True

    print(req.path)

    pathlib_path = Path(filepath)
    if ".." in pathlib_path.parts:
        resp.status = 403
        return resp

    if os.path.exists(filepath):
        ext = filepath.split('.')[-1].lower()
        if ext in ["jpeg", "jpg", "gif", "swf", "png"]:
            resp.is_binary = True
            with open(filepath, "rb") as f:
                data = f.read()
        else:
            with open(filepath, "r") as f:
                data = f.read()
    else:
        if aware_dir_enum:
            resp.status = 403
        else:
            resp.status = 404
        return resp

    if put_data:
        resp.data = data

    resp.headers.update({
        "Content-Length": len(data),
        "Content-Type": MIME_TYPES[ext],
        "Connection": "Close",
    })
    return resp

#
# def check_for_dir_escaping(filename: str):
#     pass

# if __name__ == "__main__":
# path = "/httptest"
# print(path.split('/'))
