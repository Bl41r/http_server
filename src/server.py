# -*- coding: utf-8 -*-
import socket
import sys



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


def response_error(http_exception_inst):
    return http_exception_inst.as_response()


def parse_request(req):
    header_body = req.split('\r\n' * 2, 1)
    header = header_body[0]

    try:
        body = header_body[1]
    except IndexError:
        body = ''

    status = header.split('\r\n')[0]
    header = header.split('\r\n')[1:]
    headers_split = [h.split(':', 1) for h in header]
    header_dict = {key.lower(): val.strip() for key, val in headers_split}
    req_tuple = (status, header_dict, body)

    if req_tuple[0].split()[0] != "GET":
        raise HTTPException("405", "Method Not Allowed", "<h1>GET is the only method allowed</h1>")
    if req_tuple[0].split()[2] != "HTTP/1.1":
        raise HTTPException("505", "HTTP Version Not Supported", "<h1>Fix yo shit</h1>")
    if "host" not in req_tuple[1]:
        raise HTTPException("417", "Expectation Failed", "<h1>Requires host header</h1>")

    uri = req_tuple[0].split()[1]   # for clarity
    return uri


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
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
            try:
                uri = parse_request(msg)
                conn.sendall(response_ok(uri))
            except HTTPException as e:
                conn.sendall(response_error(e).encode('utf8'))

            conn.close()
        except KeyboardInterrupt:
            print('Server interrupted.  Server shutting down.')
            server.close()
            sys.exit(0)

if __name__ == '__main__':
    server()
