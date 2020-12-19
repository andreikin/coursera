

import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))


    def put(self, metric, val, timestamp=None):
        timestamp = timestamp or int(time.time())
        message = ' '.join(['put', metric, str(val), str(timestamp)])
        print(message)
        self.socket.sendall(message.encode("utf8"))

    def get(self, metric):
        while True:
            message = "get " + metric
            self.socket.send(message.encode("utf8"))
            data = self.socket.recv(2048)
            if data:
                print(data.decode("utf8"))
                return data

#from  client import *
cl = Client("127.0.0.1", 10001)
cl.put("metrica", 452)
#cl.get("palm.cpu")
#python D:\03_andrey\coursera\diving_into_python\client.py