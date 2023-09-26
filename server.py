import socket
import time


class server:
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address: str = '0.0.0.0'
    server_port: int = 9001
    user_hashmap: dict[str, list]= {}
    message: str = ''

    def __init__(self) -> None:
        pass

    # サーバのアドレスをソケットに紐付ける
    def set_sock_bind(self) -> None:
        self.sock.bind((self.server_address, self.server_port))

    # クライアントからデータを受信する
    def receive(self) -> bytes:
        print('\nwaiting to receive message')
    
        # 型ヒントを指定
        receive_data: bytes
        address: str
        username: str

        receive_data, address = self.sock.recvfrom(4096)
        send_data: bytes= receive_data
        receive_data_str: str= receive_data.decode()
        username, self.message = receive_data_str.split(':')
        time_start: float= time.perf_counter()
        self.user_hashmap[username] = [address,time_start]

        return send_data

    # 一定時間メッセージを送信していないclientをhashmapから削除する
    def time_over_delete(self) -> None:
        for user in self.user_hashmap.keys():
            if time.perf_counter() - self.user_hashmap[user][1] >= 60:
                self.user_hashmap[user][0] = ''

    # データをクライアントに送り返す
    def send(self,send_data) -> None:
        for user in self.user_hashmap.keys():
            if self.user_hashmap[user][0] != '':
                sent: int = self.sock.sendto(send_data, self.user_hashmap[user][0])

    # ソケットを閉じてリソースを解放する
    def close(self) -> None:
        print('closing socket')
        self.sock.close()

    # chatでやりとりする
    def chat_start(self) -> None:
        try:
            while True:
                send_data: bytes = self.receive()

                self.time_over_delete()

                self.send(send_data)

                if self.message == 'server_exit':
                    break
        finally:
            self.close()

def main() -> None:
    server_info :server = server()
    server_info.set_sock_bind()
    server_info.chat_start()


if __name__ == '__main__':
    main()