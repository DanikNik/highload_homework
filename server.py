import asyncio
from httparse import Request, Response
from handler import handle_request


async def handle_client(reader, writer):
    data_in = await reader.read(512)
    message = data_in.decode()
    # addr = writer.get_extra_info('peername')

    request = Request()
    request.parse(message)
    resp = handle_request(request)
    data_out = bytes(resp.to_string(), encoding="UTF-8")
    writer.write(data_out)
    # if resp.is_binary:
    writer.write(resp.data)
    await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_client, '127.0.0.1', 8000, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
