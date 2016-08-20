# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    (u'morethan8', u'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nmorethan8'),
    (u'eight888', u'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\neight888'),
    (u'less8', u'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nless8'),
    (u'éyçño', u'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\néyçño'),
    (u'', u'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'),
]
STRING_TABLE = [
    ('rodstewartisagreatsinger', type(u'')),
    (b'eiaojfa;eijfa;lkvnjknzvjkhfeu', type(u'')),
    ('éyçño', type(u'')),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result


@pytest.mark.parametrize('a_string, a_type', STRING_TABLE)
def test_force_unicode(a_string, a_type):
    assert type(client.force_unicode(a_string, type(u''))) is type(u'')


def test_main():
    """Test main call without message exits system"""
    with pytest.raises(SystemExit):
        client.main()
