# -*- coding: utf-8 -*-
import socket

port = 5010


def response_ok():
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I'm sexy come on sugar let me know\r\n\r\n"


def response_error(msg):
    return "HTTP/1.1 500 Internal Server Error\r\nNO YOU SUCK IT: " + msg + "\r\n\r\n"


def parse_request(req):
    # GET localhost:5001 HTTP/1.1\r\nHost: localhost:5001\r\n\r\n
    req = req.split()
    proto = req[2]
    host = req[3] + ' ' + req[4]
    if req[0] != 'GET':
        return response_error('get')
    if proto != 'HTTP/1.1':
        return response_error('protocol')
    if host != 'Host: localhost:5001':
        return response_error('host')
    return 'Successfully parsed'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = ('127.0.0.1', port)
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
    if msg == 'suck it':
        msg = response_error()
    else:
        parse_request(msg)
        msg = response_ok()
    conn.sendall(msg)
    conn.close()
