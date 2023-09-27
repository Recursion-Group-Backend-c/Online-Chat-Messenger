import socket

server_address = "0.0.0.0"
server_port = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((server_address, server_port))
print("UDP server start up on {}".format(server_port))


client_list = set()

class Server:
    def __init__(self) -> None:
        pass
    
    
def main():    
    try:
        while True:
            print("\nWaiting to receive message")
            data, address = sock.recvfrom(4096)
            client_list.add(address)
            print("Recieved {} bytes from {}".format(len(data), address))
            print(data)
            print(client_list)
            
            if data:
                for client_address in client_list:
                    sent = sock.sendto(data, client_address)
                    print("Sent {} bytes to {}".format(sent, client_address))
                
    except KeyboardInterrupt as err:
        print("\n Closing server !!!")
        print("\n ", str(err))
        socket.close()
    
    
if __name__ == "__main__":
    main()