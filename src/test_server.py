# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    ('GET localhost:5000 HTTP/1.1\r\nHost: localhost:5000\r\n\r\n'),

]



@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result
