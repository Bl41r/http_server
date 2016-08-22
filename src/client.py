# -*- coding: utf-8 -*-
import socket
import sys


def make_GET(url):
    return 'GET /sample.txt HTTP/1.1\r\nHost: ' + url + '\r\n\r\n'


def init_connection(ip, port):
    infos = socket.getaddrinfo(ip, port)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    return client


def send_msg():
    client = init_connection('127.0.0.1', 5020)
    client.sendall(make_GET('localhost:5020').encode('utf8'))

    client.shutdown(socket.SHUT_WR)
    reply_complete = False
    res = b''
    buffer_length = 8

    while not reply_complete:
        part = client.recv(buffer_length)
        res += part
        if len(part) < buffer_length:
            reply_complete = True

    client.close()
    print('recv\'d: ', res)
    res = res.decode('utf8')
    return res


def main():
    if len(sys.argv) != 1:
        print(u'usage: python3 client.py')
        sys.exit(1)
    else:   # pragma: no cover
        return send_msg()


if __name__ == '__main__':  # pragma: no cover
    main()
