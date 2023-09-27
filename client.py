import socket
import threading
import random

# need type here
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ポート番号がランダムで割り振られる、よっぽど運悪くなきゃダブらない…ハズ
client.bind(("localhost", random.randint(8081, 9999)))

name: str = input("NickName: ")


def receive() -> None:
    while True:
        try:
            # need type here
            message, _ = client.recvfrom(4096)
            print(message.decode())
        except:
            pass


# need type here
t = threading.Thread(target=receive)
t.start()

client.sendto(f"Nickname:{name}".encode(), ("localhost", 8080))

while True:
    message: str = input("")
    if message == "exit":
        # CI変更はないが、接続が切られるはず。
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 8080))
