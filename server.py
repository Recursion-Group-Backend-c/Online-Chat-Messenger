import socket
import threading
import queue
from datetime import datetime, timedelta
from typing import TypedDict


class Client(TypedDict):
    addr: str
    timer: datetime


messages: queue.Queue = queue.Queue()

clients: Client = {}

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
