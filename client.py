import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('localhost', 8888, loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

if __name__ == "__main__":
    message = 'Hello World!'
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(tcp_echo_client(message + str(i), loop)) for i in range(1000)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
