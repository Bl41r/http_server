# -*- coding: utf-8 -*-
import socket
import sys

port = 5010


def split_headers(res):
    pass


def make_GET(url):
    # GET /path/file.html HTTP/1.1
    return 'GET ' + url + ' HTTP/1.1\r\nHost: ' + url + '\r\n\r\n'


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


def send_msg():
    client, stream_info = init_connection('127.0.0.1', port)
    client.connect(stream_info[-1])

    #try:
    #    client.sendall(msg.encode('utf8'))
    #except UnicodeDecodeError:
    #    client.sendall(msg)

    client.sendall(make_GET('localhost:5001').encode('utf8'))

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
    try:
        res = res.decode('utf8')
    except:
        pass
    print('final:', res)
    return res


def main():
    if len(sys.argv) != 1:
        print(u'usage: python3 client.py')
        sys.exit(1)
    else:
        send_msg()

if __name__ == '__main__':
    main()
