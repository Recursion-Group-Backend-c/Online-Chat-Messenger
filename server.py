import socket
import threading
import queue

messages: queue.Queue = queue.Queue()
# need type
clients = []

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
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("Nickname:"):
                        name: str = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)


# need type
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
