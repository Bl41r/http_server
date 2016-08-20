# -*- coding: utf-8 -*-
import socket
import sys

port = 5002


def split_headers(res):
    try:
        res = res.decode('utf8')
    except AttributeError:
        pass
    header = res.split('\r\n\r\n')[0]
    if len(res.split('\r\n\r\n')) > 1:
        body = res.split('\r\n\r\n')[1]
    else:
        body = ""
    status = header.split('\r\n')[0]
    header = header.split('\r\n')[1:]
    headers_split = [h.split(':', 1) for h in header]
    header_dict = {key.lower(): val.strip() for key, val in headers_split}
    print('split headers returns: ', (status, header_dict, body))
    return (status, header_dict, body)


def make_GET(url):
    return 'GET / HTTP/1.1\r\nHost: ' + url + '\r\n\r\n'


def init_connection(ip, port):
    infos = socket.getaddrinfo(ip, port)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    return client, stream_info


def send_msg():
    client, stream_info = init_connection('127.0.0.1', port)
    client.connect(stream_info[-1])

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
    split_headers(res)
    res = res.decode('utf8')
    return res


def main():
    if len(sys.argv) != 1:
        print(u'usage: python3 client.py')
        sys.exit(1)
    else: # pragma: no cover
        return send_msg()

if __name__ == '__main__': # pragma: no cover
    main()
