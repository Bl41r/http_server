import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = ('127.0.0.1', 5019)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(address)

server.listen(1)
conn, addr = server.accept()

buffer_length = 8
message_complete = False

msg = ''
while not message_complete:
    part = conn.recv(buffer_length)
    msg += part.decode('utf-8')
    if len(part) < buffer_length or not part:
        message_complete = True
        break

print('recvd:', msg)
conn.sendall(msg.encode('utf-8'))
conn.shutdown(1)
conn.close()
