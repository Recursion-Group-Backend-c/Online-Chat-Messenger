import socket
import sys
import time
import threading
import getpass


class UDPClient:
    def __init__(self, username, port, address="0.0.0.0", buffer=4096) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serverAddress = '0.0.0.0'
        self.__serverPort = 9010
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
                sent = self.__socket.sendto(bMessage,(self.__serverAddress, self.__serverPort))
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

    
    def checkTime(self):
        try:    
            while True:
                currenttime = time.time()
                if currenttime - self.__lastSenttime > 600:
                    self.__connection = False
                    break
                time.sleep(1)
        except TimeoutError as e:
            print("セッション有効期限が切れました。")
            print(e)
        finally:
            print("接続時間が切れました。")
            self.close()
            
        
    def close(self):
        print("Closing socket")
        self.__socket.close()



class TCPClient:
    def __init__(self, buffer=4096) -> None:
        self.__tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverAddress = "0.0.0.0"
        self.__serverPort = 9001
        self.__buffer = buffer
        self.__accessToken = ""
        
    def start(self):
        print("Connecting to {}".format(self.__serverAddress, self.__serverPort))
        self.connect()
        self.send()
        
    def connect(self):
        try:
            self.__tcpsocket.connect((self.__serverAddress, self.__serverPort))
        except socket.error as e:
            print("ソケットエラー", e)
            sys.exit(1)
            
    def send(self):
        operationFlag = True
        while operationFlag:
            operation = input("1: You want to make Room.\n2: You want to join ChatRoom\n")
            operation = int(operation)
            if operation ==1 or operation == 2:
                operationFlag = False
            else:
                print("Input Proper Num")
        state = ""
        
        if operation == 1:
            state = 0
        else:
            state = 9
        
        try:
            while True:
                if operation == 1:
                    print("operation == 1")
                    # TCP接続確立後のヘッダー送信
                    password = "password"
                    header = self.chatroom_protocol(5, operation, state, "room1", password)
                    self.__tcpsocket.send(header)
                    flagPass = True
                    
                    # while flagPass:
                    #     password1 = getpass.getpass("input your password : ")
                    #     if password1 == getpass.getpass("input your password one more time : "):
                    #         flagPass = False
                    #         password = password1
                    #     else:
                    #         print("Wrong password. please set password one more time")
                    
                    response1 = self.__tcpsocket.recv(32)
                    room_name_size, operation, state, room_name, status1 = self.get_server_response_of_header(response1)
                    print(room_name_size, operation, state, room_name, status1)
                    if state == 1:
                        print("リクエストの応答(1): サーバーから応答がありました。")
                        
                    response2 = self.__tcpsocket.recv(32)
                    room_name_size, operation, state, room_name, status2 = self.get_server_response_of_header(response2)
                    print(room_name_size, operation, state, room_name, status2)
                    if state == 2:
                        # roomName = input("input room name where you want to join : ")
                        header = self.chatroom_protocol(5, operation, state, "room1", "")
                        self.__tcpsocket.send(header)
                        print("send!!")
                        print("リクエストの応答(2): 部屋が作成されました")
                    response3 = self.__tcpsocket.recv(32)
                    room_name_size, operation, state, room_name, status3 = self.get_server_response_of_header(response3)
                    print(room_name_size, operation, state, room_name, status3 )
                    break
                
                        
                elif operation == 2:
                    # TCP接続確立後のヘッダー送信
                    password = ""
                    header = self.chatroom_protocol(0, operation, state, "", "")
                    self.__tcpsocket.send(header)
                    
                    roomName = input("input Room Name you want to join in : ")
                    password = input("input Password : ")
                    
                    join_roomName_password = self.chatroom_protocol(5, operation, state, roomName, password)
                    self.__tcpsocket.send(join_roomName_password)
                    
                    response1 = self.__tcpsocket.recv(32)
                    room_name_size, operation, state, room_name, status1 = self.get_server_response_of_header(response1)
                    print(room_name_size, operation, state, room_name, status1)
                    
                    self.__tcpsocket.send(header)
                    flagPass = True
                    break
            self.close()
            # UDP通信開始
            threading.Thread(target=UDPClient.send())
            
        except TimeoutError:
            print("Socket timeout, ending listning for serever messages")
                
            
    def get_server_response_of_header(self, data):
        # data = connection.recv(32)
        room_name_size =int.from_bytes(data[:1], "big")
        operation = int.from_bytes(data[1:2], "big")
        state = int.from_bytes(data[2:3], "big")
        room_name = data[3:11].decode("utf-8").replace(" ","")
        password = data[11:].decode("utf-8").replace(" ","")
        
        return (room_name_size, operation, state, room_name, password)
    
    def chatroom_protocol(self, room_name_size:int, operation:int, state:int, room_name:str, password:str):
        if len(room_name.encode("utf-8")) < 8:
            room_name = room_name.ljust(8, " ")
        
        if len(password.encode("utf-8")) < 21:
            password = password.ljust(21, " ")

        return room_name_size.to_bytes(1, "big") + \
            operation.to_bytes(1, "big") + \
            state.to_bytes(1, "big") + \
            room_name.encode("utf-8") + \
            password.encode("utf-8")

            
    def close(self):
        print("Closing socket")
        self.__socket.close()
            
            
def main():
    tcplient = TCPClient()
    tcplient.start()
    port = input("input port address : ")
    username = input("Input your userName : ")
    udpclient = UDPClient(username, port)
    udpclient.start()
    
if __name__ == "__main__":
    main()