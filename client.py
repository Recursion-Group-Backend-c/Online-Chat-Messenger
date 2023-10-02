import socket
import threading
import random
import uuid
import struct

# need type
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ポート番号がランダムで割り振られる、よっぽど運悪くなきゃダブらない…ハズ
client.bind(("localhost", random.randint(8081, 9999)))

name: str = input("NickName: ")


def receive() -> None:
    while True:
        try:
            # need type
            message, _ = client.recvfrom(4094)
            print(message.decode())
        except:
            pass


# need type
t = threading.Thread(target=receive)
t.start()

# TEMP
# udp header packaged with struct
udpHeader: struct = struct.pack("!BB", RoomNameSize, TokenSize)

client.sendto(udpHeader.encode() + f"Nickname:{name}".encode(), ("localhost", 8080))

while True:
    message: str = input("")
    if message == "exit":
        # CI変更はないが、接続が切られるはず。
        exit()
    else:
        client.sendto(udpHeader.encode() + f"{name}: {message}".encode(), ("localhost", 8080))
