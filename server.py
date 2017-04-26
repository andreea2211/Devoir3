Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import sys
import socket
import select

# get local machine name

host = socket.gethostname()

socketlist = []
recvbuffer = 2048
port = 6666

def chat_server():
    
# creation d'un objet socket

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # lier au port

    serversocket.bind((host, port))

    # la file d'attente jusqu'à cinq demandes

    serversocket.listen(5)

    socketlist.append(serversocket)

    while True:
        ready_to_read, ready_to_write, in_error = select.select(socketlist, [], [], 0)

        for sock in ready_to_read:
            if sock == serversocket:
                
                # etablir la connexion

                clientsocket, addr = serversocket.accept()
                
                socketlist.append(clientsocket)

                print("Connection du client avec IP %s" % str(addr))

                broadcast(serversocket, clientsocket, "[%s:%s] est en ligne\n" % addr)
            else:
                try:
                    data = sock.recv(recvbuffer)
                    if data:
                        broadcast(serversocket, sock, "\r" + '[' + str(sock.getpeername()) + ']' + data)
                    else:
                        if sock in socketlist:
                            socketlist.remove(sock)
                            
                        broadcast(serversocket, sock, "Client (%s, %s) est hors ligne\n" % addr)
                        
                except:
                    broadcast(serversocket, sock, "Client (%s, %s) est hors ligne\n" % addr)
                    continue
                
        clientsocket.close()

    serversocket.close()

def broadcast(serversocket, sock, message):
    for socket in socketlist:
        if socket != serversocket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in socketlist:
                    socketlist.remove(socket)

if _name_ == "close":
    sys.exit(chat_server())
