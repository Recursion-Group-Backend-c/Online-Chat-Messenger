import socket

class Client:
    def __init__(self, address, port=8080, buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverAddress = '0.0.0.0'
        self.__serverPort = 9001
        self.__address = address
        self.__port = port
        self.__buffer = buffer
    
    def start(self):
        print("Starting up on {} ".format(self.__serverPort))
        self.__socket.bind((self.__address, self.__port))
        self.sendandrecive()
        
    def sendandrecive(self):
        try:
            message = input("Input your message which you wanna send ? : ")
            bMessage = bytes(message, "utf-8")
            
            # サーバーへデータを送信
            sent = self.__socket.sendto(bMessage,(self.__serverAddress, self.__serverPort))
            print('send {} bytes'.format(sent))
            
            # 応答を受信
            print("Waiting to recive")
            data, server = self.__socket.recvfrom(self.__buffer)
            print("Recived {!r}".format(data))
            
        finally:
            self.close() 
        
    def close(self):
        print("Closing socket")
        

def main():
    client_address = input("input your client address : ")
    # port = 8080
    client = Client(client_address)
    client.start()
     
if __name__ == "__main__":
    main()