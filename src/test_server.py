# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    ('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I\'m sexy come on sugar let me know\r\n\r\n')
]
RES_TABLE = [
    ('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I\'m sexy come on sugar let me know\r\n\r\n', ('HTTP/1.1 200 OK', {'content-type': 'text/plain'}, "If you want my body and you think I'm sexy come on sugar let me know"))
]


@pytest.mark.parametrize('result', MSG_TABLE)
def test_send_msg(result):
    """Test to see that message sent is returned"""
    assert client.send_msg() == result


@pytest.mark.parametrize('res, result', RES_TABLE)
def test_split_headers(res, result):
    """Test to see that response is not byte code"""
    assert client.split_headers(res) == result


def test_init_connection_error():
    """Test error raises when receiving bad stream info"""
    with pytest.raises(client.socket.gaierror):
        client.init_connection('poop', 5000)


def test_main():
    """Test main exits system without proper command"""
    with pytest.raises(SystemExit):
        client.main()
