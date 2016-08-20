# -*- coding: utf-8 -*-
import socket

port = 5003


class HTTPException(Exception):
    def __init__(self, code, reason, htmlstring):
        self.code = code
        self.reason = reason
        self.htmlstring = htmlstring

    def as_response(self):
        template = "HTTP/1.1 {} {}\r\n\r\n{}"
        return template.format(self.code, self.reason, self.htmlstring)


def response_ok(uri):
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I'm sexy come on sugar let me know\r\n\r\n"


def response_error(msg):
    return msg


def parse_request(req):
    header = req.split('\r\n\r\n')[0]
    if len(req.split('\r\n\r\n')) > 1:
        body = req.split('\r\n\r\n')[1]
    else:
        body = ""
    status = header.split('\r\n')[0]
    header = header.split('\r\n')[1:]
    headers_split = [h.split(':', 1) for h in header]
    header_dict = {key.lower(): val.strip() for key, val in headers_split}
    req_tuple = (status, header_dict, body)
    if req_tuple[0].split()[0] != "GET":
        return response_error(HTTPException("405", "Method Not Allowed", "<h1>GET is the only method allowed</h1>").as_response())
    if req_tuple[0].split()[2] != "HTTP/1.1":
        return response_error(HTTPException("505", "HTTP Version Not Supported", "<h1>Fix yo shit</h1>").as_response())
    if "host" not in req_tuple[1]:
        return response_error(HTTPException("417", "Expectation Failed", "<h1>Requires host header</h1>").as_response())

    return response_ok(req_tuple[0].split()[1])


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
        try:
            new_msg = parse_request(msg).encode('utf8')
        except AttributeError:
            new_msg = parse_request(msg)
    conn.sendall(new_msg)
    conn.close()
