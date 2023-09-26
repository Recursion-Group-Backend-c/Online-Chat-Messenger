import socket
import threading

class client:
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address: str = '0.0.0.0'
    server_port: int = 9001
    client_port: int = 8080
    send_exit_flag = False
    receive_exit_flag = False

    def __init__(self, client_address: str, username: str) -> None:
        self.client_address = client_address
        self.username = username

    # クライアントのアドレスをソケットに紐付ける
    def set_sock_bind(self) -> None:
        self.sock.bind((self.client_address, self.client_port))

    # CLIからの入力をサーバに送信する
    def send(self) -> None:
        while True:
            message: str = input()
            send_data: bytes = (f'{self.username}:{message}').encode()
            sent: int = self.sock.sendto(send_data,(self.server_address,self.server_port))

            if self.chat_exit('send', message):
                break

    # サーバからデータを受け取ってメッセージを表示する
    def receive(self) -> None:
        while True:
            # 型ヒントを指定
            receive_data: bytes
            receive_username: str
            receive_message: str

            receive_data, _ = self.sock.recvfrom(4096)
            receive_data_str: str = receive_data.decode()
            receive_username,receive_message = receive_data_str.split(':')

            print('{} : {}'.format(receive_username,receive_message))

            if self.chat_exit('receive', receive_message):
                break

    # クライアントのチャットを終了させる
    def chat_exit(self, func_name: str, message: str) -> bool:
        if(message == 'client_exit'):
            if(func_name == 'send'):
                self.send_exit_flag = True
            elif(func_name == 'receive'):
                self.receive_exit_flag = True
        return self.send_exit_flag and self.receive_exit_flag

    # ソケットを閉じてリソースを解放する
    def close(self) -> None:
        print('closing socket')
        self.sock.close()

    # chatでやりとりする
    def chat_start(self) -> None:
        try:
            print('Chat start!\nHow to exit\nclient : client_exit\nserver : server_exit\n')
            # スレッド作成
            thread_send: threading.Thread = threading.Thread(target=self.send)
            thread_receive: threading.Thread = threading.Thread(target=self.receive)

            # スレッドの処理を開始する
            thread_send.start()
            thread_receive.start()

            # スレッドの処理を待つ
            thread_send.join()
            thread_receive.join()

        finally:
            self.close()

def main() -> None:
    client_address: str = input('Input your address : ')
    username: str = input('Input username : ')
    
    client_info: client = client(client_address, username)
    client_info.set_sock_bind()
    client_info.chat_start()


if __name__ == '__main__':
    main()