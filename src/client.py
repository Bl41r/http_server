# -*- coding: utf-8 -*-
import socket
import sys


def force_unicode(a_string):
    if sys.version_info.major == 3:
        text_type = str
    else:   # pragma: no cover
        text_type = type(u'')
    if not isinstance(a_string, text_type):
        return a_string.decode('utf-8')
    return a_string


def init_connection(ip, port):
    infos = socket.getaddrinfo(ip, port)
    try:
        stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    except IndexError:  # pragma: no cover
        print('Error aquiring stream_info.')
        sys.exit(1)
    else:
        client = socket.socket(*stream_info[:3])
        client.connect(stream_info[-1])
        return client


def send_msg(msg):

    msg = force_unicode(msg)

    client = init_connection('127.0.0.1', 5004)
    client.sendall(msg.encode('utf8'))
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
    print('decoded message: ', res)
    return res


def main():
    if len(sys.argv) != 2:
        print(u'usage: python3 client.py "message to send"')
        sys.exit(1)
    else:   # pragma: no cover
        send_msg(sys.argv[1])

if __name__ == '__main__':  # pragma: no cover
    main()
