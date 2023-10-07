import socket
import sys
import re

import protocol


class tcp_client:
    def __init__(self) -> None:
        self.__socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_address: str = "localhost"
        self.__server_port: int = 9001
        self.__buffer: int = 32
        self.__host_token_buffer: int = 128
        self.__room_name_size: int = 1
        self.__operation: int = 1
        self.__state: int = 0
        self.__room_name: str = ""
        self.__password: str = ""
        self.__host_token: str = ""
        self.__user_name: str = ""
        

    def is_valid_str_len(self,input,num) -> bool:
        l: int = len(input)
        return  0 < l and l <= num

    def is_valid_password(self) -> bool:
        return self.__password.find(" ") == -1 and \
            len(self.__password) >= 6 and \
            len(self.__password) <= 11 and \
            re.search("[0-9]",self.__password) != None and \
            re.search("[A-Z]",self.__password) != None and \
            re.search("[a-z]",self.__password) != None

    def set_input(self) -> None:
        while not self.is_valid_str_len(10):
            self.__user_name = input("Input user name(Up to 10 characters) : ")
        self.__operation = int(input("Input operation(choose 1 or 2) : "))
        while not self.is_valid_str_len(8):
            self.__room_name = input("Input room name(Up to 8 characters) : ")
        while not self.is_valid_password():
            print("Password conditions.\n" + \
                "Must be between 6 and 11 characters and include the following characters.\n" + \
                "・Uppercase letters\n" + \
                "・Lowercase letters\n" + \
                "・NumbersInput")
            self.__password = input("Input password : ")
        self.__room_name_size = int(input("Input room name size (Range 0 to 255): ")) if self.__operation == 1 else 0
        self.__host_token = input("Input host token : ") if self.__operation == 2 else ""

    def set_init(self) -> None:
        self.__room_name_size = 1
        self.__operation = 1
        self.__state = 0
        self.__room_name = ""
        self.__password = ""
        self.__host_token = ""
        self.__user_name = ""

    def start(self) -> None:
        print("Connecting to {}{}".format(self.__server_address, self.__server_port))
        
        try:
            self.__socket.connect((self.__server_address, self.__server_port))
        except socket.error as err:
            print(err)
            sys.exit(1)
        
        self.communication()

    def communication(self) -> None:
        try:
            while True:
                self.set_input()

                header: bytes = protocol.protocol_header(self.__room_name_size, self.__operation, self.__state, self.__room_name, self.__user_name, self.__password)
                self.__socket.send(header)
                
                # ルームを作成する
                if self.__operation == 1:
                    print("state : {}".format(self.__state))

                    recv_header1: bytes = self.__socket.recv(self.__buffer)
                    self.__state = protocol.get_state(recv_header1)
                    self.__password = ""
                    print("state : {}".format(self.__state))

                    recv_header2: bytes = self.__socket.recv(self.__buffer)
                    self.__state = protocol.get_state(recv_header2)
                    print("state : {}".format(self.__state))

                    self.__host_token = self.__socket.recv(self.__host_token_buffer).decode("utf-8")
                    print("host_token : {} \nPlease note this down as it will be used for room invitations.\n".format(self.__host_token))

                    break

                # ルームに参加する
                elif self.__operation == 2:
                    self.__socket.send(self.__host_token.encode("utf-8"))

                    message: str = self.__socket.recv(self.__buffer).decode("utf-8")
                    # 成功
                    if message == "success":
                        print("Chat room: {} successfully created\n".format(self.__room_name))
                        break
                    # 失敗_ルームの許容人数に達している
                    elif message == "failed_roomsize_over":
                        print("Could not join room.\nThe room capacity has been reached\n")
                    # 失敗_パスワードが正しくない
                    elif message == "failed_wrong_password":
                        print("Could not join room.\nPlease review your password\n")
                    
                    # 初期化
                    self.set_init()
                           
        finally:
            self.close()
            
    def close(self) -> None:
        print("Closing socket")
        self.__socket.close()

def main() -> None:
    client: tcp_client = tcp_client()
    client.start()


if __name__ == "__main__":
    main()
