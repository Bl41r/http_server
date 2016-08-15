import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = ('127.0.0.1', 5000)
server.bind(address)

server.listen(1)
conn, addr = server.accept()

buffer_length = 8
message_complete = False

while not message_complete:
    part = conn.recv(buffer_length)
    print(part.decode('utf-8'))
    if len(part) < buffer_length:
        message_complete = True
print(part)

conn.sendall(part.encode('utf-8'))
conn.close()
server.close()
