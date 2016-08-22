# -*- coding: utf-8 -*-
import pytest
import client
import mimetypes
from server import response_ok, response_error, parse_request, HTTPException, resolve_uri, sanitize_uri

MSG_TABLE = [
    ('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Size: 95\r\n\r\nThis is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n\r\n\r\n')
]


def test_sanitize_uri():
    """Test substitution of ~ or .. for empty string"""
    assert sanitize_uri('./webroot/..') == './webroot/'
    assert sanitize_uri('./webroot/~') == './webroot/'


def test_resolve_uri_404():
    """Test returns file not found."""
    with pytest.raises(IndexError):
        resolve_uri('/fake.txt') == 'IndexError: The file you requested does not exist.'


def test_parse_request():
    """Tests parse request function returns uri."""
    assert parse_request("GET / HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n\r\n") == '/'


def test_response_ok():
    """Test response_ok func."""
    assert response_ok(('test', 'test', 'test')) == b"HTTP/1.1 200 OK\r\nContent-Type: test\r\nContent-Size: test\r\nHost: 127.0.0.1:5020\r\n\r\ntest\r\n\r\n"


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
