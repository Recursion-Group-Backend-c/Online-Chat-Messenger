import socket
import threading
import queue
from datetime import datetime, timedelta
from typing import TypedDict
from uuid import uuid4


# TEMP
class Client:
    def __init__(self, _addr: str, _timer: datetime, _token: uuid4):
        self.addr = _addr
        self.timer = datetime.now() + timedelta(minutes=10)
        self.token = uuid4()

    def sendToken(self):
        server.sendto(self.token.encode(), self.addr)


# TEMP
class Room:
    def __init__(self, _name: str, _host: Client, _clientList: list[Client]):
        self.name = _name
        self.host = _host
        self.clientList = _clientList

    def closeRoom(self):
        self.client = []


# TEMP
class ClientDict(TypedDict):
    addr: str
    timer: datetime


# TEMP
class TokenDict(TypedDict):
    addr: str
    token: uuid4


messages: queue.Queue = queue.Queue()

clients: ClientDict = {}

server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 8080))


def receive():
    while True:
        try:
            # need type
            message, addr = server.recvfrom(4096)
            messages.put((message, addr))
        except:
            pass


def broadcast():
    while True:
        while not messages.empty():
            # need type
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients[addr] = datetime.now() + timedelta(minutes=10)
            for client in list(clients.keys()):
                try:
                    if datetime.now() > clients[client]:
                        server.sendto(b'session timedout, start over the program to connect again', client)
                        del clients[client]
                    elif message.decode().startswith("Nickname:"):
                        name: str = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                        clients[client] = datetime.now() + timedelta(minutes=10)
                    else:
                        server.sendto((str(datetime.now().time())[:8] + "   ").encode() + message, client)
                        clients[client] = datetime.now() + timedelta(minutes=10)
                except:
                    del clients[client]


# need type
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
