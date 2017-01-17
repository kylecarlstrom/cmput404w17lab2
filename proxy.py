# Based on code from Joshua Cambell
#!/usr/bin/env python

import socket, os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reuse the address even if it is in use (doesn't always work)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 0.0.0.0 means every address on this machine
serverSocket.bind(("0.0.0.0", 8000))
serverSocket.listen(5) # Accept at most 5 incoming connections in a queue

while True:
    (incomingSocket, address) = serverSocket.accept()
    print("We got a connection from %s" % str(address))
    if os.fork() == 0:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # socket.AF_INET indicates that we want an IPv4 socket
        # socket.SOCK_STREAM indicates that we want a TCP socket

        clientSocket.connect(("www.google.com", 80))

        incomingSocket.setblocking(0)
        clientSocket.setblocking(0)

        while True:
            request = bytearray()
            while True:
                try:
                    part = incomingSocket.recv(1024)
                except IOError, e:
                    if e.errno == socket.errno.EAGAIN:
                        part = None
                    else:
                        raise
                if (part):
                    clientSocket.sendall(part)
                    request.extend(part)
                else:
                    break

            if len(request) > 0:
                print(request)

            response = bytearray()
            while True:
                try:
                    part = clientSocket.recv(1024)
                except IOError, e:
                    if e.errno == socket.errno.EAGAIN:
                        part = None
                    else:
                        raise
                if (part):
                    incomingSocket.sendall(part)
                    response.extend(part)
                else:
                    break
            
            if len(response) > 0:
                print(response)