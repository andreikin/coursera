

import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        #self.socket = socket.socket()
        #self.socket.connect((self.host, self.port))


    def put(self, metric, val, timestamp=None):
        timestamp = timestamp or int(time.time())
        message = ' '.join(['put', metric, str(val), str(timestamp)])
        #print(message)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.connect((self.host, self.port))

            sock.settimeout(self.timeout)
            sock.sendall(message.encode("utf8"))
            sock.send(message.encode())
            data = sock.recv(1024).decode()

        if data == 'error\nwrong command\n\n':
            raise ClientError()

    def get(self, metric):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            message = "get " + metric
            sock.send(message.encode("utf8"))
            data = sock.recv(2048)
            if data:
                print(data.decode("utf8"))
                return data

#from  client import *
cl = Client("127.0.0.1", 10001)
cl.put("metrica", 452)
#cl.get("palm.cpu")
#python D:\03_andrey\coursera\diving_into_python\client.py