import socket
import sys




def send_msg(msg):
    infos = socket.getaddrinfo('127.0.0.1', 5005)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(msg.encode('utf-8'))
    buffer_length = 8
    reply_complete = False
    while not reply_complete:
        part = client.recv(buffer_length)
        print(part.decode('utf-8'))
        if len(part) < buffer_length:
            reply_complete = True
    client.close()
    print('lookie: ', part)


def main():
    if len(sys.argv) != 2:
        print(u'usage: python3 client.py <message to send>')
        sys.exit(1)
    else:
        send_msg(sys.argv[1])

if __name__ == '__main__':
    main()