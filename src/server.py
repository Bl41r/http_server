# -*- coding: utf-8 -*-
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = ('127.0.0.1', 5000)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(address)
server.listen(1)

while True:
    conn, addr = server.accept()

    buffer_length = 8
    message_complete = False

    msg = ''
    while not message_complete:
        part = conn.recv(buffer_length)
        msg += part.decode('utf8')
        if len(part) < buffer_length or not part:
            message_complete = True

    print('recvd:', msg)
    conn.sendall(msg.encode('utf8'))
    conn.close()
