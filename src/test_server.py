# -*- coding: utf-8 -*-
import pytest
import client
from server import response_ok, response_error

MSG_TABLE = [
    ('morethan8', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nmorethan8'),
    ('eight888', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\neight888'),
    ('less8', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nless8'),
    ('éyçño', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + u'éyçño'),
    ('', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'),
]
STRING_TABLE = [
    ('rodstewartisagreatsinger'),
    (b'eiaojfa;eijfa;lkvnjknzvjkhfeu'),
    ('éyçño'),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned."""
    assert client.send_msg(msg) == result


@pytest.mark.parametrize('a_string', STRING_TABLE)
def test_force_unicode(a_string):
    """Test type is forced to unicode."""
    assert type(client.force_unicode(a_string)) is type(u'')


def test_main():
    """Test main cal without message exits system."""
    with pytest.raises(SystemExit):
        client.main()


def test_response_ok():
    """Test response ok sends proper status line."""
    assert response_ok() == b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"


def test_response_error():
    """Test response error is returned."""
    assert response_error() == b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
