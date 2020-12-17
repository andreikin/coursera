
"""import asyncio
async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001, loop=loop)
    print("send: {}".format(message))
    writer.write(message.encode())
    writer.close()
loop = asyncio.get_event_loop()
message = "ping232"
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()"""

import socket

class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.connect(self.host, self.port)

    def put(self, metric, val, timestamp=None):
        self.socket.sendall(metric+":"+str(val).encode("utf8"))

    def get(self):
        pass



socket = socket.create_connection(("127.0.0.1", 10001))
socket.sendall("ping".encode("utf8"))
socket.close()