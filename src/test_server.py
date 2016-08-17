# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    (u'morethan8', u'morethan8'),
    (u'eight888', u'eight888'),
    (u'less8', u'less8'),
    ('éyçño', u'éyçño'),
    (u'', u''),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result
