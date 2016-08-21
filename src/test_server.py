# -*- coding: utf-8 -*-
import pytest
import client
from server import response_ok, response_error, parse_request, HTTPException

MSG_TABLE = [
    ('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I\'m sexy come on sugar let me know\r\n\r\n')
]
RES_TABLE = [
    ('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I\'m sexy come on sugar let me know\r\n\r\n', ('HTTP/1.1 200 OK', {'content-type': 'text/plain'}, "If you want my body and you think I'm sexy come on sugar let me know"))
]


def test_parse_request():
    """Tests parse request function returns uri."""
    assert parse_request("GET / HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n\r\n") == '/'


def test_response_ok():
    """Test response_ok func."""
    assert response_ok('test') == b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nIf you want my body and you think I'm sexy come on sugar let me know\r\n\r\n"


def test_response_error():
    """Test response_error func."""
    test_case = HTTPException("405", "Method Not Allowed", "<h1>GET is the only method allowed</h1>")
    assert response_error(test_case) == "HTTP/1.1 405 Method Not Allowed\r\n\r\n<h1>GET is the only method allowed</h1>"


@pytest.mark.parametrize('result', MSG_TABLE)
def test_send_msg(result):
    """Test to see that message sent is returned."""
    assert client.send_msg() == result


def test_init_connection_error():
    """Test error raises when receiving bad stream info."""
    with pytest.raises(client.socket.gaierror):
        client.init_connection('poop', 5000)


def test_main():
    """Test main exits system without proper command."""
    with pytest.raises(SystemExit):
        client.main()
