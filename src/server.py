# -*- coding: utf-8 -*-
import socket
import sys


def response_ok():
    """Sends a well formed response suitable for socket transmission."""
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"


def response_error():
    return b"HTTP/1.1 500 Internal Server Error\r\n\r\n"


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5005)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(1)

    while True:
        try:
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
            if msg == 'error':
                msg = response_error()
            else:
                msg = response_ok() + msg.encode('utf8')
            conn.sendall(msg)
            conn.close()
        except KeyboardInterrupt:
            print('Server interrupted. Server shutting down.')
            server.close()
            sys.exit(0)


if __name__ == '__main__':
    server()
