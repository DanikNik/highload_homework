import socket

import config
from worker import Worker
import multiprocessing

if __name__ == "__main__":
    conf = config.Config()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 8090))
    sock.listen(512)
    sock.setblocking(False)
    print("Server is running at {}".format(sock.getsockname()))

    conf.read_config()
    workers = []

    for x in range(int(conf.config_data["cpu_limit"])):
        worker = multiprocessing.Process(
            target=Worker(
                sock=sock,
                config_data=conf.config_data
            ).run)
        workers.append(worker)
        worker.start()
        print("Worker {} loaded...".format(x+1))

    try:
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for worker in workers:
            print("Terminating worker {}".format(worker.pid))
            worker.terminate()
    sock.close()
    print("Stopping the server")
