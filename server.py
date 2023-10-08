import socket

# server_address = '0.0.0.0'
# server_port = 9001
# print('starting up on port {}'.format(server_port))

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # ソケットを特殊なアドレス0.0.0.0とポート9001に紐付け
# sock.bind((server_address, server_port))
# print("UDP server start up on {}".format(server_port))


client_list = set()

class Server:
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
                print("\nWaiting to recive message")
                data, client_address = self.__socket.recvfrom(self.__buffer)
                
                print("Recived {} bytes from {}".format(len(data), client_address))
                print(data)
                
                if data:
                    sent = self.__socket.sendto(data, client_address)      
                    print('Sent {} bytes back to {}'.format(sent, client_address))  
        finally:
            self.close()
    
    def close(self):
        print("Closing server")
        self.__socket.close
    
    
    
    
def main():    
    address = "0.0.0.0"
    port = 9001
    server = Server(address, port)
    server.start()

    
if __name__ == "__main__":
    main()