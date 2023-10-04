import socket
import sys
import time
import re

import protocol


class Client:
    def __init__(self) -> None:
        self.__socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverAddress: str = "localhost"
        self.__serverPort: int = 9001
        self.__buffer: int = 4096
        self.__room_name_size: int = 1
        self.__operation: int = 1
        self.__state: int = 0
        self.__room_name: str = ""
        self.__password: str = ""
        self.__host_token: str = ""
        self.__member_token: str = ""
    
    def is_valid_room_name(self) -> bool:
        return len(self.__room_name) <= 8

    def is_valid_password(self) -> bool:
        return self.__password.find(" ") == -1 and \
            len(self.__password) >= 6 and \
            len(self.__password) <= 21 and \
            re.search("[0-9]",self.__password) != None and \
            re.search("[A-Z]",self.__password) != None and \
            re.search("[a-z]",self.__password) != None

    def set_input(self) -> None:
        self.__operation = int(input("input operation(choose 1 or 2) : "))
        while not self.is_valid_room_name():
            self.__room_name = input("Input room name(Up to 8 characters) : ")
        while not self.is_valid_password():
            print("Password conditions.\n" + \
                "Must be between 6 and 21 characters and include the following characters.\n" + \
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

    def start(self) -> None:
        print("Connecting to {}{}".format(self.__serverAddress, self.__serverPort))
        
        try:
            self.__socket.connect((self.__serverAddress, self.__serverPort))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.communication()

    def communication(self) -> None:
        try:
            while True:
                self.set_input()

                header: bytes = protocol.protocol_header(self.__room_name_size, self.__operation, self.__state, self.__room_name, self.__password)
                self.__socket.send(header)
                
                if self.__operation == 1:
                    recv_header1: bytes = self.__socket.recv(self.__buffer)
                    self.__state = protocol.get_state(recv_header1)
                    self.__password = ""
                    print("state : {}".format(self.__state))

                    recv_header2: bytes = self.__socket.recv(self.__buffer)
                    self.__state = protocol.get_state(recv_header2)
                    print("state : {}".format(self.__state))

                    self.__host_token = self.__socket.recv(self.__buffer).decode("utf-8")
                    print("host_token : {}".format(self.__host_token))

                    break

                elif self.__operation == 2:
                    time.sleep(1)
                    self.__socket.send(self.__host_token.encode("utf-8"))

                    message: str = self.__socket.recv(self.__buffer).decode("utf-8")
                    if message == "success":
                        self.__member_token = self.__socket.recv(self.__buffer).decode("utf-8")
                        print("member_token : {}".format(self.__member_token))
                        break
                    elif message == "failed_roomsize_over":
                        print("Could not join room.\nThe room capacity has been reached")
                    elif message == "failed_wrong_password":
                        print("Could not join room.\nPlease review your password")
                    
                    self.set_init()
                           
        finally:
            self.close()
            
    def close(self) -> None:
        print("Closing socket")
        self.__socket.close()

def main() -> None:
    client: Client = Client()
    client.start()


if __name__ == "__main__":
    main()
