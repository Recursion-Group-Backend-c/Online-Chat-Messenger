import socket
import threading
import time

class Client:
    def __init__(self, username, port, address="0.0.0.0", buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverAddress = '0.0.0.0'
        self.__serverPort = 9001
        self.__username = username
        self.__address = address
        self.__port = int(port)
        self.__buffer = buffer
        self.__lastSenttime = time.time()
        self.__connection = True
    
    def start(self):
        print("Starting up on {} ".format(self.__serverPort))
        print(self.__address, self.__port)
        self.__socket.bind((self.__address, self.__port))
        thread_send = threading.Thread(target=self.send)
        thread_recive = threading.Thread(target = self.recive)
        thread_checkConnectiontime = threading.Thread(target=self.checkTime)

        try:
            while self.__connection:
                thread_checkConnectiontime.start()
                thread_send.start()
                thread_send.join()
                thread_checkConnectiontime.join()
                thread_recive.start()
                thread_recive.join()
            
        except KeyboardInterrupt as e:
            print("keyboardInterrrupt called!" + str(e))
            
        except OSError as e:
            print("OS Error ! " + str(e))
            
        finally:
            self.close()    
        
    def send(self):
        while self.__connection:
            try:
                message = input("Input message your messsage : ")
                if message == "exit":
                    break
                
                if not message:
                    print("No message please input again\n")
                    continue
                
                bMessage = bytes(self.__username + " : " + message, "utf-8")
                
                # サーバーへデータを送信
                sent = self.__socket.sendto(bMessage, (self.__serverAddress, self.__serverPort))
                print('send {} bytes'.format(sent))
                self.__lastSenttime = time.time()
            
            except KeyboardInterrupt as e:
                print("keyboardInterrrupt called!" + str(e))
                break
            
    
    def recive(self):
        try:
            while self.__connection:
                print("Waiting to recive....")
                data, server = self.__socket.recvfrom(self.__buffer)
                print("Recived {!r}".format(data))
            print("接続が切れました。")
        except KeyboardInterrupt as e:
            print("keyboard interuppted !!!", str(e))
        except OSError as e:
            print("OS Error ! " + str(e))
        # finally:
        #     self.__socket.close()
        
    
    def checkTime(self):
        try:    
            while True:
                currenttime = time.time()
                if currenttime - self.__lastSenttime  > 600:
                    self.__connection = False
                    break
                time.sleep(1)
        except TimeoutError as e:
            print("セッション有効期限が切れました。")
            print(e)
        finally:
            print("時間切れです。通信を終了します。")
            self.close()
            
        
    def close(self):
        print("Closing socket")
        self.__socket.close()
        

def main():
    # client_address = input("input your client address : ")
    port = input("input port address : ")
    username = input("Input your userName : ")
    client = Client(username, port)
    client.start()
    
if __name__ == "__main__":
    main()