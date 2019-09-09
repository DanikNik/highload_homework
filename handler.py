from httparse import Request, Response


def handle_request(req: Request):
    if req.method == "HEAD":
        return make_response(False)
    elif req.method == "GET":
        return make_response(True)
    else:
        return Response(status=405)
    pass


def make_response(put_data: bool):
    resp = Response(headers={
        "Server": "pinx",
    })
    return resp


def read_file(filename):
    pass
