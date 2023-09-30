import socket



class ChatRoom:
    def __init__(self) -> None:
        pass
    
    

class Server:
    def __init__(self, address:str, port:int, buffer:int=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = address
        self.__port = port
        self.__buffer = buffer
        
    def start(self):
        self.__socket.bind((self.__address, self.__port))
        print("Starting up on {} port {}".format(self.__address, self.__port))
        self.__socket.listen(1)
        self.recive()
        
    def recive(self):
        connection, client_address = self.__socket.accept()
        try:
            while True:
                try:
                    print("Connection from {}".format(client_address))
                    data = connection.recv(self.__buffer)
                    data_str = data.decode("utf-8")
                    print("Recived data : {} ".format(data_str))
                    if data:
                        response = "Processing : " + data_str
                        connection.sendall(response.encode())
                        print("Send backed to client: ", response)
                    else:
                        print("No data from {}".format(client_address))
                        break
                    
                except Exception as e:
                    print("Error: " + str(e))
            
        finally:
            self.close(connection)
            
    def close(self, connection):
        print("Closing current connection")
        connection.close()
    

def main():    
    address = '0.0.0.0'
    port = 9001
    server = Server(address, port)
    server.start()

    
if __name__ == "__main__":
    main()