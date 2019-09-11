import asyncio
import socket

import uvloop as uvloop

import config
from httparse import Request, Response
# from handler import handle_request
from datetime import datetime
from pytz import timezone
from pathlib import Path
import os
import urllib

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

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def get_time_now_http():
    return timezone('Europe/Moscow').localize(datetime.now()).strftime("%a, %d %b %Y %H:%M:%S %Z")


class Worker:
    def __init__(self, sock: socket.socket, config_data: dict):
        # self.loop = asyncio.get_event_loop()
        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.sock = sock
        self.config_data = config_data

    # @asyncio.coroutine
    async def handle_client(self, conn: socket.socket):
        data_in = await self.loop.sock_recv(conn, 512)
        message = data_in.decode()
        request = Request()
        request.parse(message)
        resp = await self.handle_request(request)
        data_out = bytes(resp.headers_to_string(), encoding="UTF-8")
        await self.loop.sock_sendall(conn, data_out)
        await self.loop.sock_sendall(conn, resp.data)
        conn.close()

    def run(self):
        self.loop.run_until_complete(self.run_worker_process())
        # self.loop.run_forever()

    async def run_worker_process(self):
        while True:
            conn, _ = await self.loop.sock_accept(self.sock)
            conn.settimeout(10)
            conn.setblocking(False)
            self.loop.create_task(self.handle_client(conn))

    async def handle_request(self, req: Request) -> Response:
        if req.method == "HEAD":
            return await self.make_response(req, False)
        elif req.method == "GET":
            return await self.make_response(req, True)
        else:
            return Response(status=405)
        pass

    async def make_response(self, req: Request, put_data: bool) -> Response:
        resp = Response(headers={
            "Server": "py_nginx",
            "Date": get_time_now_http()
        })

        document_root = self.config_data["document_root"]

        filepath = os.path.join(document_root, req.path.lstrip('/'))
        filepath = urllib.parse.unquote(filepath)
        aware_dir_enum = False
        if filepath[-1] == '/':
            filepath = os.path.join(filepath, "index.html")
            aware_dir_enum = True

        pathlib_path = Path(filepath)
        if ".." in pathlib_path.parts:
            resp.status = 403
            return resp

        if os.path.exists(filepath):
            ext = str(filepath).split('.')[-1].lower()
            with open(filepath, "rb") as f:
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

    def stop(self):
        pass
