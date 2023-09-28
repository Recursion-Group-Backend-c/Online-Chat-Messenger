import socket
import threading

class Client:
    def __init__(self, username, port, address="0.0.0.0", buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverAddress = '0.0.0.0'
        self.__serverPort = 9001
        self.__username = username
        self.__address = address
        self.__port = int(port)
        self.__buffer = buffer
    
    def start(self):
        print("Starting up on {} ".format(self.__serverPort))
        print(self.__address, self.__port)
        self.__socket.bind((self.__address, self.__port))
        thread_send = threading.Thread(target=self.send)
        thread_recive = threading.Thread(target = self.recive)

        try:
            thread_recive.start()
            thread_send.start()
            thread_send.join()
            thread_recive.join()
            
        except KeyboardInterrupt as e:
            print("keyboardInterrrupt called!" + str(e))
            
        finally:
            self.close()    
        
    def send(self):
        while True:
            try:
                message = input("Input your message which you wanna send ? : ")
                if message == "exit":
                    break
                
                if not message:
                    print("No message please input again\n")
                    continue
                
                bMessage = bytes(self.__username + " : " + message, "utf-8")
                
                # サーバーへデータを送信
                sent = self.__socket.sendto(bMessage,(self.__serverAddress, self.__serverPort))
                print('send {} bytes'.format(sent))
            
            except KeyboardInterrupt as e:
                print("keyboardInterrrupt called!" + str(e))
                break
    
    def recive(self):
        # 応答を受信
        try:
            while True:
                print("Waiting to recive....")
                data, server = self.__socket.recvfrom(self.__buffer)
                print("Recived {!r}".format(data))
        except KeyboardInterrupt as e:
            print("keyboard interuppted !!!", str(e))
                
            
    def close(self):
        print("Closing socket")
        

def main():
    # client_address = input("input your client address : ")
    port = input("input port address : ")
    username = input("Input your userName : ")
    client = Client(username, port)
    client.start()
     
if __name__ == "__main__":
    main()