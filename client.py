
>>> """
Dan Andreea
1221F
"""

import sys
import socket
import select

def chat_client():

    # create a socket object

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)

    # obtenir le nom de la machine locale

    host = socket.gethostname()

    port = 6666

    try:
        # connexion au nom du host sur le port
        
        s.connect((host, port))
        
    except:
        print "Connexion impossible"
        sys.exit()


    print "Connection realisee. Tapez le message..."
    sys.stdout.write('<Moi>'); sys.stdout.fush()

    while True:
        socketlist = [sys.stdin, s]
        ready_to_read, ready_to_write, in_error = select.select(socketlist, [], [])

        for sock in ready_to_read:
            if sock == s:
                
                # Recevoir plus de 1024 octets

                tm = s.recv(1024)

                if not tm:
                    print "\n Deconnecte du serveur"
                    sys.exit()
                else:
                    sys.stdout.write(tm)
                    sys.stdout.write('<Moi>'); sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('<Moi>'); sys.stdout.flush()



if _name_ == "close":
    sys.exit(chat_client())
