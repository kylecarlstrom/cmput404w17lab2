# Based on code from Joshua Cambell
#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.AF_INET indicates that we want an IPv4 socket
# socket.SOCK_STREAM indicates that we want a TCP socket

clientSocket.connect(("www.google.com", 80))
# note that there is no http:// because we are working at a low enough level that the application layer doesn't matter
# we pass in a tuple with web url and a port
# port 80 is the stand port for http

# command, / is location on the server
request = "GET / HTTP/1.0\r\n\r\n"

clientSocket.sendall(request)

response = bytearray()

while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print(response)