import socket


class Server: 
    client_list = set()
    
    def __init__(self, address, port, buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = address
        self.__port = port
        self.__buffer = buffer
        
    def start(self):
        #  ソケットを特殊なアドレス0.0.0.0とポート9001に紐付け
        self.__socket.bind((self.__address, self.__port))
        print("UDP server start up on {} port: {}".format(self.__address, self.__port))
        self.recvAndSend()     
    
    def recvAndSend(self):
        try:
            while True:
                try:
                    print("\nWaiting to recive message")
                    data, client_address = self.__socket.recvfrom(self.__buffer)
                    str_data = data.decode("utf-8")
                    
                    print("Recived {} bytes from {}".format(len(data), client_address))
                    [userName, messagedata] = str_data.split(":")
                    Server.client_list.add(client_address)
                    
                    if data:
                        print(Server.client_list)
                        for c_address in Server.client_list:
                            # print("address: ",c_address)
                            sent = self.__socket.sendto(data, c_address)      
                            print('Sent {} bytes back to {}'.format(sent, c_address))
                
                except KeyboardInterrupt:
                    print("\n KeyBoardInterrupted!")
                    break
                
        finally:
            self.close()
    
    def close(self):
        print("Closing server")
        self.__socket.close
    
    
    
    
def main():    
    address = '0.0.0.0'
    port = 9001
    server = Server(address, port)
    server.start()

    
if __name__ == "__main__":
    main()