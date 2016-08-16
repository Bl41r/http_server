import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = ('127.0.0.1', 5005)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(address)

server.listen(1)
conn, addr = server.accept()

buffer_length = 8
message_complete = False

msg = ''
while not message_complete:
    part = conn.recv(buffer_length)
    print(part.decode('utf-8'))
    if len(part) < buffer_length or len(part) % buffer_length != 0:
        print('in if')
        message_complete = True
        break
    msg += part.decode('utf-8')

print(msg)
print('got here')
conn.sendall(msg.encode('utf-8'))
print('sent')
conn.close()
server.close()
