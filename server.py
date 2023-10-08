import socket
import struct
import sys
import threading
import time
import random
import uuid

import protocol


class memberUser:
    def __init__(self, member_token: str = '', user_name: str = '', ip_address: str = '') -> None:
        self.member_token: str = member_token
        self.user_name: str = user_name
        self.ip_address: str = ip_address

        self.start_time: float = sys.float_info.max
    
    def set_start_time(self,time: float ):
        self.start_time = time

class hostUser:
    def __init__(self, host_token: str = '', room_name: str = '', room_name_size: int = 0, user_name: str = '', ip_address: str = '', password: str = '') -> None:
        self.host_token: str = host_token
        self.room_name: str = room_name
        self.room_name_size: int = room_name_size
        self.user_name: str = user_name
        self.ip_address: str = ip_address
        self.password: str = password

        self.start_time: float = sys.float_info.max
    
    def set_start_time(self,time: float ):
        self.start_time = time

class room:
    member_user_list: list[memberUser] = []

    def __init__(self, host_user: hostUser = hostUser() ) -> None:
        self.host_user = host_user
    
    def set_member_user(self,member_user: memberUser) -> None:
        self.member_user_list.append(member_user)

class roomList:
    room_list: list[room] = []

    def __init__(self) -> None:
        pass

class tcpServer:
    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = '0.0.0.0'
        self.server_port: int = 9001
        self.buffer: int = 32

        self.room_name_size: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ''
        self.password: str = ''
        self.host_token: str = ''
        self.user_name: str = ''
        self.member_token: str = ''

        self.socket.bind((self.server_address, self.server_port))
        print('[TCP]Starting up on {} ,port {}'.format(self.server_address, self.server_port))
        self.socket.listen(1)

    def set_header(self,header):
        self.room_name_size = protocol.get_room_name_size(header)
        self.operation = protocol.get_operation(header)
        self.state = protocol.get_state(header)
        self.room_name = protocol.get_room_name(header)
        self.password = protocol.get_password(header)

    def set_init(self) -> None:
        self.room_name_size = 1
        self.operation = 1
        self.state = 0
        self.room_name = ''
        self.password = ''
        self.host_token = ''
        self.user_name = ''

    def communication(self):
        while True:
            connection, client_address = self.socket.accept()
            try:
                while True:
                    print('[TCP]Connection from {}'.format(client_address))
                    self.set_header(connection.recv(self.buffer))

                    # ルームを作成する
                    if self.operation == 1:
                        self.state = 1

                        connection.send(protocol.protocol_header(self.room_name_size, \
                                                                    self.operation, \
                                                                    self.state, \
                                                                    self.room_name, \
                                                                    self.user_name, \
                                                                    self.password))

                        # ホストトークンを発行する
                        self.host_token = str(uuid.uuid4())

                        # ルームを作成する
                        chat_host_user = hostUser(self.host_token, \
                                                                self.room_name, \
                                                                self.room_name_size, \
                                                                self.user_name, \
                                                                socket.inet_ntoa(struct.pack('>I', random.randrange(0x7F000001, 0x7FFFFFFE))), \
                                                                self.password)
                        chat_room = room(chat_host_user)
                        chat_room_list.room_list.append(chat_room)

                        self.state = 2

                        connection.send(protocol.protocol_header(self.room_name_size, \
                                                                    self.operation, \
                                                                    self.state, \
                                                                    self.room_name, \
                                                                    self.user_name, \
                                                                    self.password))
                        connection.send(self.host_token.encode('utf-8'))
                        connection.send(chat_host_user.ip_address.encode('utf-8'))

                        break
                    
                    # ルームに参加する
                    elif self.operation == 2:
                        self.host_token = connection.recv(36).decode('utf-8')

                        # send_message
                        # 0 : 成功 
                        # 1 : 失敗_クライアントから通知したホストトークンが存在しない
                        # 2 : 失敗_ルームの許容人数に達している
                        # 3 : 失敗_パスワードが正しくない
                        send_message = '1'
                        send_address = ''

                        # ルームに参加できるかチェックする処理
                        for i in range(len(chat_room_list.room_list)):
                            c_room = chat_room_list.room_list[i]
                            
                            if self.host_token != c_room.host_user.host_token:
                                continue
                            elif c_room.host_user.room_name_size < len(c_room.member_user_list) + 2:
                                send_message = '2'

                            elif self.password != c_room.host_user.password:
                                send_message = '3'
                            else:
                                # メンバートークンを発行する
                                self.member_token = str(uuid.uuid4())

                                # メンバーを追加する
                                chat_member_user = memberUser(self.member_token, \
                                                                self.user_name, \
                                                                socket.inet_ntoa(struct.pack('>I', random.randrange(0x7F000001, 0x7FFFFFFE))))
                                c_room.set_member_user(chat_member_user)
                                send_message = '0'
                                send_address = chat_member_user.ip_address
                                
                        connection.send(send_message.encode('utf-8'))

                        if send_message == '0':
                            connection.send(send_address.encode('utf-8'))
                            break

                        self.set_init()
                
            except Exception as err:
                print('[TCP]Error: ' + str(err))

            finally:
                self.close(connection)

    def close(self, connection):
        print('[TCP]Closing current connection\n')
        connection.close()

class udp_server:
    def __init__(self) -> None:
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address: str = 'localhost'
        self.server_port: int = 9002
        self.client_port: int = 8080
        self.buffer: int = 4096

        self.message: str = ''

        self.host_token: str = ''
        self.user_name: str = ''
        self.client_address: str = ''

    def set_sock_bind(self) -> None:
        self.sock.bind((self.server_address, self.server_port))

    def receive(self) -> bytes:
        print('[UDP]waiting to receive message')
    
        # 型ヒントを指定
        receive_data: bytes
        
        receive_data, (self.client_address, _) = self.sock.recvfrom(self.buffer)
        receive_data_str: str= receive_data.decode()
        self.host_token,self.user_name,self.message = receive_data_str.split(':')
        
        send_data: bytes = (f'{self.user_name}:{self.message}').encode()
        
        self.user_delete()

        return send_data

    # 一定時間メッセージを送信していないまたはユーザが自ら退出したい場合リレーシステムから削除する
    def user_delete(self) -> None:
        for i in range(len(chat_room_list.room_list)):
            h_user = chat_room_list.room_list[i].host_user
            m_user = chat_room_list.room_list[i].member_user_list

            if self.host_token == h_user.host_token:
                if self.client_address == h_user.ip_address and (time.time() - h_user.start_time >= 60 or self.message == 'exit'):
                    chat_room_list.room_list.pop(i)

                for j in range(len(m_user)):
                    if self.client_address == m_user[j].ip_address and (time.perf_counter() - m_user[j].start_time >= 60 or self.message == 'exit'):
                        m_user.pop(j)

    def send(self,send_data) -> None:
        for i in range(len(chat_room_list.room_list)):
            h_user = chat_room_list.room_list[i].host_user
            m_user = chat_room_list.room_list[i].member_user_list
            
            if self.host_token == h_user.host_token:
                h_sent: int = self.sock.sendto(send_data, (h_user.ip_address, self.client_port))
                h_user.set_start_time(time.time())

                for j in range(len(m_user)):
                    m_sent: int = self.sock.sendto(send_data, (m_user[j].ip_address, self.client_port))

                    if self.client_address == m_user[j].ip_address:
                        m_user[j].set_start_time(time.time())

    def close(self) -> None:
        print('[UDP]closing socket\n')
        self.sock.close()

    def chat_start(self) -> None:
        self.set_sock_bind()

        try:

            while True:
                send_data: bytes = self.receive()

                self.send(send_data)
        finally:
            self.close()

chat_room_list: roomList = roomList()
chat_host_user: hostUser = hostUser()
chat_member_user: memberUser = memberUser()
chat_room: room = room()

def main():
    tcp_chat_server = tcpServer()
    udp_chat_server = udp_server()

    # スレッド作成
    thread_tcp = threading.Thread(target=tcp_chat_server.communication)
    thread_udp = threading.Thread(target=udp_chat_server.chat_start)

    # スレッドの処理を開始する
    thread_tcp.start()
    thread_udp.start()

    # スレッドの処理を待つ
    thread_tcp.join()
    thread_udp.join()


if __name__ == '__main__':
    main()
