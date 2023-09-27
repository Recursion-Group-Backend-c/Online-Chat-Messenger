import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = "0.0.0.0"
server_port = 9001


address = ''
port = 9050

# UserName
userName = input("Input your userName? : ")
buserName = bytes(userName, "utf-8")
# Message Send
message = input("Input your message you want to sent? : ")
bMessage =  bytes(message, 'utf-8')

sock.bind((address,port))

try:
    print("Sending {!r}".format(bMessage))

    sentuserName = sock.sendto(buserName, (server_address, server_port))
    sentMessage = sock.sendto(bMessage, (server_address, server_port))
    print("Send {} bytes ".format(sentuserName))
    print("Send {} bytes ".format(sentMessage))

    
    # 応答を受信
    print("Waiting receive")
    data, server = sock.recvfrom(4096)
    print("Recieved {!r}".format(data))
    
finally:
    print("Closing socket")
    sock.close()