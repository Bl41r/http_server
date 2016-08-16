import socket
import sys

def init_connection():
    infos = socket.getaddrinfo('127.0.0.1', 5019)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    return client, stream_info

def send_msg(msg):
    client, stream_info = init_connection()
    client.connect(stream_info[-1])
    client.sendall(msg.encode('utf-8'))
    client.shutdown(1)

    reply_complete = False
    res = ''
    buffer_length = 8

    while not reply_complete:
        part = client.recv(buffer_length)
        part = part.decode('utf-8')
        res += part
        if len(part) < buffer_length:
            reply_complete = True
            break

    client.close()
    print('recvd: ', res)
    return res


def main():
    if len(sys.argv) != 2:
        print(u'usage: python3 client.py "message to send"')
        sys.exit(1)
    else:
        send_msg(sys.argv[1])

if __name__ == '__main__':
    main()