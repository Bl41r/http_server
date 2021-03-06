# -*- coding: utf-8 -*-
import socket
import sys
import io
import os
import mimetypes
import re


class HTTPException(Exception):
    def __init__(self, code, reason, htmlstring):
        self.code = code
        self.reason = reason
        self.htmlstring = htmlstring

    def as_response(self):
        template = "HTTP/1.1 {} {}\r\n\r\n{}"
        return template.format(self.code, self.reason, self.htmlstring)


def response_ok(uri):
    print('URI', uri)
    tmp = "HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Size: {}\r\nHost: 127.0.0.1:5020\r\n\r\n{}\r\n\r\n".format(uri[0], uri[2], uri[1])
    return tmp.encode('utf8')


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
        raise HTTPException("505", "HTTP Version Not Supported", "<h1>Currently supports 1.1</h1>")
    if "host" not in req_tuple[1]:
        raise HTTPException("417", "Expectation Failed", "<h1>Requires host header</h1>")

    uri = (req_tuple[0].split()[1])   # for clarity
    return uri


def sanitize_uri(parsed_uri):
    parsed_uri = re.sub('\.\.', '', parsed_uri)
    parsed_uri = re.sub('~', '', parsed_uri)
    return parsed_uri


def resolve_uri(parsed_uri):
    root = u"./webroot"
    parsed_uri = root + parsed_uri
    parsed_uri = sanitize_uri(parsed_uri)
    try:
        file_type = mimetypes.guess_type(parsed_uri)
        f = io.open(parsed_uri, encoding=file_type[1])
        body = f.read()
        f.close()
        file_size = os.path.getsize(parsed_uri)
        return (file_type[0], body, file_size)
    except IsADirectoryError:
        if os.path.exists(parsed_uri):
            filenames = os.listdir(parsed_uri)
            body = ''
            for filename in filenames:
                path = os.path.join(parsed_uri, filename)
                body += "<h1>" + path + "</h1>\n"
            body += '</html>'
            return ("text/directory", body, 0)
        else:
            raise IndexError("This directory does not exist.")
    except FileNotFoundError:
        if parsed_uri == "./webroot/favicon.ico":
            return ("icon", "empty", 0)
        else:
            raise IndexError("The file you requested does not exist.")
    # update response ok function to accomplish this task


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5020)
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
                resolved_uri = resolve_uri(uri)
                conn.sendall(response_ok(resolved_uri))
            except HTTPException as e:
                conn.sendall(response_error(e).encode('utf8'))

            conn.close()
        except KeyboardInterrupt:
            print('Server interrupted.  Server shutting down.')
            server.close()
            sys.exit(0)

if __name__ == '__main__':
    server()
