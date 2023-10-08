import socket
import sys
import threading
import re

import protocol


class tcp_client:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = 'localhost'
        self.server_port: int = 9001
        self.buffer: int = 32
        self.host_token_buffer: int = 36
        self.client_address: str = ''

        self.room_name_size: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ''
        self.password: str = ''
        self.host_token: str = ''
        self.user_name: str = ''
        
    def is_valid_str_len(self,input,num) -> bool:
        l: int = len(input)
        return  0 < l and l <= num

    def is_valid_password(self) -> bool:
        return self.password.find(' ') == -1 and \
            len(self.password) >= 6 and \
            len(self.password) <= 11 and \
            re.search('[0-9]',self.password) != None and \
            re.search('[A-Z]',self.password) != None and \
            re.search('[a-z]',self.password) != None

    def set_input(self) -> None:
        while not self.is_valid_str_len(self.user_name,10):
            self.user_name = input('Input user name(Up to 10 characters) : ')
        self.operation = int(input('Input operation(choose 1 or 2) : '))
        while not self.is_valid_str_len(self.room_name,8):
            self.room_name = input('Input room name(Up to 8 characters) : ')
        while not self.is_valid_password():
            print('Password conditions.\n' + \
                'Must be between 6 and 11 characters and include the following characters.\n' + \
                '・Uppercase letters\n' + \
                '・Lowercase letters\n' + \
                '・NumbersInput')
            self.password = input('Input password : ')
        self.room_name_size = int(input('Input room name size (Range 0 to 255): ')) if self.operation == 1 else 0
        self.host_token = input('Input host token : ') if self.operation == 2 else ''

    def set_init(self) -> None:
        self.room_name_size = 1
        self.operation = 1
        self.state = 0
        self.room_name = ''
        self.password = ''
        self.host_token = ''
        self.user_name = ''

    def start(self) -> None:       
        try:
            self.socket.connect((self.server_address, self.server_port))
        except socket.error as err:
            print(err)
            sys.exit(1)
        
        self.communication()

    def communication(self) -> None:
        try:
            while True:
                self.set_input()

                self.socket.send(protocol.protocol_header(self.room_name_size, \
                                                            self.operation, \
                                                            self.state, \
                                                            self.room_name, \
                                                            self.user_name, \
                                                            self.password))
                
                # ルームを作成する
                if self.operation == 1:
                    print('create a room\nstate : {}'.format(self.state))

                    self.state = protocol.get_state(self.socket.recv(self.buffer))
                    self.password = ''
                    print('state : {}'.format(self.state))

                    self.state = protocol.get_state(self.socket.recv(self.buffer))
                    print('state : {}\nroom created!'.format(self.state))

                    self.host_token = self.socket.recv(self.host_token_buffer).decode('utf-8')
                    print('host_token : {} \nPlease note this down as it will be used for room invitations.'.format(self.host_token))

                    self.client_address = self.socket.recv(self.buffer).decode('utf-8')

                    break

                # ルームに参加する
                elif self.operation == 2:
                    self.socket.send(self.host_token.encode('utf-8'))

                    message: str = self.socket.recv(1).decode('utf-8')
                    
                    # 成功
                    if message == '0':
                        print('Chat room: {} successfully created\n'.format(self.room_name))
                        self.client_address = self.socket.recv(self.buffer).decode('utf-8')
                        break
                    # 失敗_クライアントから通知したホストトークンが存在しない
                    elif message == '1':
                        print('Could not join room.\nThe host token notified by the client does not exist\n')
                    # 失敗_ルームの許容人数に達している
                    elif message == '2':
                        print('Could not join room.\nThe room capacity has been reached\n')
                    # 失敗_パスワードが正しくない
                    elif message == '3':
                        print('Could not join room.\nPlease review your password\n')
                    
                    # 初期化
                    self.set_init()
                           
        finally:
            self.close()
            
    def close(self) -> None:
        print('Closing socket\n')
        self.socket.close()

class udp_client:
    def __init__(self,client_address: str, host_token: str, user_name: str) -> None:
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address: str = 'localhost'
        self.server_port: int = 9002
        self.client_port: int = 8080
        self.buffer: int = 4094

        self.client_address: str = client_address
        self.host_token: str = host_token
        self.user_name: str = user_name

    def set_sock_bind(self) -> None:
        self.sock.bind((self.client_address, self.client_port))

    def send(self) -> None:
        print('Please enter your message.\nIf you want to leave, please enter "exit"\n')
        while True:
            # メッセージを送信する
            message: str = input()
            send_data: bytes = (f'{self.host_token}:{self.user_name}:{message}').encode()
            sent: int = self.sock.sendto(send_data,(self.server_address,self.server_port))

    def receive(self) -> None:
        while True:
            # 型ヒントを指定
            receive_data: bytes
            receive_username: str
            receive_message: str

            receive_data, _ = self.sock.recvfrom(self.buffer)
            receive_data_str: str = receive_data.decode()
            receive_username,receive_message = receive_data_str.split(':')

            print('{} : {}'.format(receive_username,receive_message))

    def close(self) -> None:
        print('closing socket\n')
        self.sock.close()

    def chat_start(self) -> None:
        self.set_sock_bind()

        try:
            print('Chat start!')
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
    tcp_client_chat: tcp_client = tcp_client()
    tcp_client_chat.start()

    udp_client_chat: udp_client = udp_client(tcp_client_chat.client_address, tcp_client_chat.host_token, tcp_client_chat.user_name)
    udp_client_chat.chat_start()


if __name__ == '__main__':
    main()
