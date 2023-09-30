import socket
import sys


def chatroom_protocol(room_name_size, operation, state, operation_payload_size):
    return room_name_size.to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + operation_payload_size.to_bytes(29, "big")


class Client:
    def __init__(self, buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverAddress = "0.0.0.0"
        self.__serverPort = 9001
        self.__buffer = buffer
        
    def start(self):
        print("Connecting to {}".format(self.__serverAddress, self.__serverPort))
        try:
            self.__socket.connect((self.__serverAddress, self.__serverPort))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.send()
            
    def send(self):
        try:
            data = input("input text to send: ")
            data_bytes = bytes(data, "utf-8")
            self.__socket.send(data_bytes)
            
            try:
                data = str(self.__socket.recv(self.__buffer))
                #  if data:
                print("Server response : {}".format(data))
                    # else:
                    #     break
            except TimeoutError:
                print("Socket timeout, ending listning for serever messages")
            
        finally:
            self.close()
            
    def close(self):
        print("Closing socket")
        self.__socket.close()
            
            

def main():
    # client_address = input("input your client address : ")
    # port = input("input port address : ")
    # username = input("Input your userName : ")
    client = Client()
    client.start()
    
if __name__ == "__main__":
    main()