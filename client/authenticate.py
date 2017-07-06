import os
import socket, ssl
from contextlib import closing

def authenticate(notes):
    thisfolder = os.path.dirname(__file__)
    servercrt = os.path.join(thisfolder, os.path.pardir, "server", "server.crt")

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ssl_socket = ssl.wrap_socket(clientsocket, 
                             ca_certs=servercrt, 
                             cert_reqs=ssl.CERT_REQUIRED)

    with closing(ssl_socket):
        #ssl_socket.connect(('localhost', 8000))
        ssl_socket.connect(("127.0.0.1", 8000)) # localhost doesn't work everywhere

        # print repr(ssl_socket.getpeername())
        # print ssl_socket.cipher()
        # print ssl_socket.getpeercert()

        msg = 'MBAUTH VERSION 002\n'
        msg += 'START\n'
        for note in notes:
            msg += note + '\n'

        msg += 'END'
        ssl_socket.write(msg)
        return ssl_socket.read()