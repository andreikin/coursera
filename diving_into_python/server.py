
# asyncio tsp server

import asyncio
import json

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 10001))
sock.listen(5)


while True:
    conn, attr = sock.accept()
    data = conn.recv(2048).decode("utf8")

    print(data)

    if "get" in data[:3]:
        data_for_send = '{"palm.cpu": [[1150864247, 0.5], [1150864248, 0.5]]}'.encode("utf8")
        conn.send(data_for_send)

# python D:\03_andrey\coursera\diving_into_python\server.py





# sock = socket.create_connection(("127.0.0.1", 10001))
# sock.sendall("ok".encode("utf8"))
# sock.close()


# async def handle_echo(reader, writer):
#     data = await reader.read(1024)
#     message = data.decode()
#     addr = writer.get_extra_info("peername")
#     print('received {} from {}'.format(message, addr))
#     writer.close()
#
#
# loop = asyncio.get_event_loop()
# coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001, loop=loop)
# server = loop.run_until_complete(coro)
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()





