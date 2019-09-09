from httparse import Request, Response
from datetime import datetime
from pytz import timezone


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
        "Date": timezone('Europe/Moscow').localize(datetime.now()).strftime("%a, %d %b %Y %H:%M:%S %Z")
    })
    return resp


def read_file(filename):
    pass


if __name__ == "__main__":
    date_naive_object = datetime.now()
    datetime_obj_pacific = timezone('Europe/Moscow').localize(date_naive_object)
    print(datetime_obj_pacific.strftime("%a, %d %b %Y %H:%M:%S %Z"))
