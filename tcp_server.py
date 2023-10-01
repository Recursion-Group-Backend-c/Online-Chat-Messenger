import socket
import time
import protocol  


class Server:
    def __init__(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = "0.0.0.0"
        self.__port = 9001
        self.__buffer = 4096
        self.__room_name_size = 1
        self.__operation = 1
        self.__state = 0
        self.__room_name = ""
        self.__password = ""
        self.__host_token = ""
        self.__member_token = ""
 
    def set_header(self,header):
        self.__room_name_size = protocol.get_room_name_size(header)
        self.__operation = protocol.get_operation(header)
        self.__state = protocol.get_state(header)
        self.__room_name = protocol.get_room_name(header)
        self.__password = protocol.get_password(header)

    def start(self):
        self.__socket.bind((self.__address, self.__port))
        print("Starting up on {} port {}".format(self.__address, self.__port))
        self.__socket.listen(1)
        self.communication()
        
    def communication(self):
        connection, client_address = self.__socket.accept()
        try:
            while True:
                try:
                    print("Connection from {}".format(client_address))
                    recv_header = connection.recv(self.__buffer)
                    self.set_header(recv_header)
                    
                    if self.__operation == 1:    
                        self.__state = 1
                        
                        send_header1 = protocol.protocol_header(self.__room_name_size, self.__operation, self.__state, self.__room_name, self.__password)
                        connection.send(send_header1)
                        time.sleep(1)
                        # [ToDo]ルームを作成する処置

                        # [ToDo]ホストトークンを発行する処置(一旦適当に書いとく)
                        self.__host_token = "host_token_generated"
                        
                        self.__state = 2
                        
                        send_header2 = protocol.protocol_header(self.__room_name_size, self.__operation, self.__state, self.__room_name, self.__password)
                        connection.send(send_header2)
                        time.sleep(1)
                        connection.send(self.__host_token.encode("utf-8"))

                        break

                    elif self.__operation == 2:
                        self.__host_token = connection.recv(self.__buffer).decode("utf-8")

                        # [ToDo]ルームに参加できるかチェックする処理

                        # [ToDo]メンバートークンを発行する処理(一旦適当に書いとく)
                        self.__member_token = "member_token_generated"

                        # [ToDo]リストトークンのリストを追跡する処理

                        send_message = "failed_wrong_password"
                        connection.send(send_message.encode("utf-8"))
                        time.sleep(1)

                        if send_message == "success":
                            connection.send(self.__member_token.encode("utf-8"))
                            break
                        
                        self.__room_name_size = 1
                        self.__operation = 1
                        self.__state = 0
                        self.__room_name = ""
                        self.__password = ""
                
                except Exception as e:
                    print("Error: " + str(e))
            
        finally:
            self.close(connection)
            
    def close(self, connection):
        print("Closing current connection")
        connection.close()


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
