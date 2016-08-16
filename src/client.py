# -*- coding: utf-8 -*-
import socket
import sys


def init_connection(ip, port):
    infos = socket.getaddrinfo(ip, port)
    try:
        stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    except IndexError:
        print('Error aquiring stream_info.')
        sys.exit(1)
    else:
        client = socket.socket(*stream_info[:3])
        return client, stream_info


def send_msg(msg):
    client, stream_info = init_connection('127.0.0.1', 5000)
    client.connect(stream_info[-1])

    try:
        client.sendall(msg.encode('utf8'))
    except UnicodeDecodeError:
        client.sendall(msg)

    client.shutdown(socket.SHUT_WR)
    reply_complete = False
    res = ''
    buffer_length = 8

    while not reply_complete:
        part = client.recv(buffer_length)
        part = part.decode('utf8')
        res += part
        if len(part) < buffer_length:
            reply_complete = True

    client.close()
    print('recv\'d: ', res)
    return res


def main():
    if len(sys.argv) != 2:
        print(u'usage: python3 client.py "message to send"')
        sys.exit(1)
    else:
        send_msg(sys.argv[1])

if __name__ == '__main__':
    main()
