# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    ('morethan8', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nmorethan8'),
    ('eight888', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\neight888'),
    ('less8', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nless8'),
    ('éyçño', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\néyçño'),
    ('', 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result
