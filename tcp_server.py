import socket
import random
import string
import threading


class UserInfo:
    def __init__(self, address, userName, isHost=False) -> None:
        self.isHost = isHost
        self.address = address
        self.userName = userName
        self.hadToken = False

class ChatRoomInfo:
    def __init__(self, roomName=None, roomPassword = None, accessToken=None,) -> None:
        self.roomName = roomName
        self.password = roomPassword
        self.accessToken = accessToken
        self.roomMember = []        
    

class Server:
    client_list = set()
    def __init__(self, tcp_address:str, tcp_port:int, udp_address:int, udp_port:int, buffer:int=4096) -> None:
        self.__tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__tcpaddress = tcp_address
        self.__tcpport = tcp_port
        self.__udpaddress = udp_address
        self.__udp_prot = udp_port
        self.__buffer = buffer
        self.__roomList = {"roomEx": ChatRoomInfo("roomEx", "password")} # roomName: ChatRoomInfo

    def generateToken(selef, size = 10):
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))        

    def udpstart(self):
        self.__udpsocket.bind((self.__udpaddress, self.__udp_prot))
        print("UDP server start up on {} port: {}".format(self.__udpaddress, self.__udp_prot))
        self.udprecvAndSend()     
    
    def udprecvAndSend(self):
        try:
            while True:
                try:
                    # print("\nWaiting to recive message")
                    data, client_address = self.__udpsocket.recvfrom(self.__buffer)
                    str_data = data.decode("utf-8")
                    
                    print("Recived {} bytes from {}".format(len(data), client_address))
                    print(data)
                    [userName, messagedata] = str_data.split(":")
                    Server.client_list.add(client_address)
                    
                    if data:
                        print(Server.client_list)
                        for c_address in Server.client_list:
                            sent = self.__udpsocket.sendto(data, c_address)      
                            print('Sent {} bytes back to {}'.format(sent, c_address))
                
                except KeyboardInterrupt:
                    print("\n KeyBoardInterrupted!")
                    break
                
        finally:
            self.udpclose()
    
    def udpclose(self):
        print("Closing server")
        self.__udpsocket.close()


    def tcp_connetcion_start(self):
        self.__tcpsocket.bind((self.__tcpaddress, self.__tcpport))
        print("Starting up on {} port {}".format(self.__tcpaddress, self.__tcpport))
        self.__tcpsocket.listen(10)
        
        while True:
            try:
                threading.Thread(target=self.tcpaccept()).start()
            except Exception as e:
                print(f'send_response: {e}')
                print('socket closing....')
                self.__tcpsocket.close()
                
    def start_chat_of_TCP(self, tcp_connection, client_address):
        # 初回のクライアントからの送信
        print("Connection from {}".format(client_address))
        
        # 状態等を送信していく。
        state = "start"
        room_name_size, operation, state, room_name, password = self.tcp_server_recive(tcp_connection)
        print(room_name_size, operation, state, room_name, password)
        
        state = "Server get your Existence"
        # header (32バイト)：RoomNameSize（1バイト） | Operation（1バイト） | State（1バイト） | OperationPayloadSize（29バイト）
        firstResponse = self.chatroom_protocol(room_name_size, operation, state, room_name, state)
        self.tcp_response(tcp_connection, firstResponse)
        
        # サーバー初期化(0)
        token = self.generateToken()
        if operation == 1:
            # リクエスト応答(1)
            state = 1
            status = "TrytoMakeRoom"
            res_make_init = self.chatroom_protocol(room_name_size, operation, state, room_name, status)
            self.tcp_response(tcp_connection, res_make_init)
            
            # リクエスト完了(2) : ルーム作成完了
            state = 2
            print("roomの作成を行います。room name {}".format(room_name))
            if not self.findRoom():
                self.makeRoom()
            else:
                print("その部屋はすでに存在します。")
                status = "Room Already Exists"
            
        elif operation == 2:
            print("join the room")
        
            
    def tcpaccept(self):
        tcp_connection, client_address = self.__tcpsocket.accept()
        try:
            self.tcp_recive(tcp_connection, client_address)
                        
        finally:
            self.tcp_close(tcp_connection)        

        
    def tcp_recive(self, tcp_connection, client_address):
        try:
            print("Connection from {}".format(client_address))
            # サーバー初期化(0)
            room_name_size, operation, state, room_name, password = self.tcp_server_recive(tcp_connection)
            # print("Recived data -->> RoomNameSize: {}, operation: {}, State: {}, roomName: {}, Password: {}".format(room_name_size, operation, state, room_name, password))
            self.tcp_response_of_server(tcp_connection, client_address ,room_name_size, operation, state, room_name, password)
            # リクエスト応答(1)
            # body -> RoomName(8 bite) + OperationPayload (21Bite)[roomname + password] ???

            #リクエストの完了 (2)
            # トークンを送信
            
        except Exception as e:
            print("Error : " + str(e))
            
    def room_init_join(self):
        pass
    
    def room_init_make(self):
        pass
                    
    def tcp_response_of_server(self, tcp_connection, client_address, room_name_size, operation, state, room_name, password):
        status = "failed"
        print(operation, type(operation))
        if (operation == 1 and state == 0):
            # リクエスト応答(1)
            state = 1
            status = "Next:MakeRoom"
            header = self.chatroom_protocol(room_name_size, operation ,state, room_name, status)
            self.tcp_response(tcp_connection, header)
            
            
            # リクエストの完了(2)
            # room作成　=> room名、password、roomHostToken設定
            status = "Made Room."
            print("roomの作成を行います。room名 {}".format(room_name))
            
            state = 2
            hostToken = self.generateToken()
            # chatRoom = ChatRoomInfo(self.__tcpaddress, self.__udpaddress, self.generateToken(), password, room_name, "Morio")
            self.makeRoom(room_name, password, client_address, "Morio")
            
            header = self.chatroom_protocol(room_name_size, operation, state, room_name, status)  
            self.tcp_response(tcp_connection, header)
            # self.tcp_close(tcp_connection)
            # self.udpstart()
        
        elif (operation == 2):
            print("部屋に入室したい。どの部屋？ Passworは?")
            
            status = "RoomName?Password?"
            header = self.chatroom_protocol(room_name_size, operation, state, room_name, status)
            self.tcp_response(tcp_connection, header)
            
            room_name_size, operation, state, room_name, password = self.tcp_server_recive(tcp_connection)
            print("部屋名、参加したいパスワードを受け取りました。", room_name_size, operation, state, room_name, password)
            if self.findRoom(room_name):
                print("部屋に入室しようとする。")
                self.joinRoom(room_name, client_address, "Morio", password)
            else:
                print("そのような部屋はありません。")
                status = "We cant find your RoomName {}".format(room_name)
            
        else:
            header = self.chatroom_protocol(room_name_size, operation, state, room_name, status)
    
    def makeRoom(self, roomName, password, address, userName):
        HostToken = self.generateToken()
        self.__roomList[roomName] = ChatRoomInfo(HostToken, password, roomName)
        Host = UserInfo(address, userName, True)
        self.__roomList[roomName].roomMember.append(Host)
        print(self.__roomList)
        for i in self.__roomList:
            print(i, self.__roomList[i].roomMember)

    
    def joinRoom(self, roomName, address, userName, password):
        status = "failed"
        # roomに入室します。
        if self.__roomList[roomName].password != password:
            print("パスワードが間違っています。")
            status = "wrong password"
        # トークン違い
        if len(self.__roomList[roomName].roomMember) > 9:
            print("部屋は満室です。入室できません。他の部屋を選んでください。")
            status = "Room is full."
        else:
            print("Roomに入室します。")
            user = UserInfo(address, userName)
            self.__roomList[roomName].roomMebmer.append(user)
            print("Roomに入室しました。")
            print(self.__roomList[roomName])
        print(self.__roomList["roomEx"])
        
            
    def findRoom(self, roomName):
        for room_n in self.__roomList:
            return roomName == room_n 
        return False
        
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
    
    def tcp_server_recive(self, tcp_connection):
        """
            サーバの初期化(0)
            Header(32): RoomNameSize(1) | Operation(1) | State(1) | room_name() | password()
        """
        data = tcp_connection.recv(32)
        print(data)
        room_name_size =int.from_bytes(data[:1], "big")
        operation = int.from_bytes(data[1:2], "big")
        state = int.from_bytes(data[2:3], "big")
        room_name = data[3:11].decode("utf-8").replace(" ","")
        password = data[11:].decode("utf-8").replace(" ","")
        
        return (room_name_size, operation, state, room_name, password)
    
    
    def tcp_response(self, tcp_connection, data):
        tcp_connection.sendall(data)
       
            
    def tcp_close(self, tcp_connection):
        print("Closing current tcp_connection")
        tcp_connection.close()
    

def main():    
    tcpaddress = '0.0.0.0'
    tcpport = 9001
    udpaddress = "0.0.0.0"
    udpport = 9010
    server = Server(tcpaddress, tcpport, udpaddress, udpport)
    
    server.tcp_connetcion_start()

    
if __name__ == "__main__":
    main()