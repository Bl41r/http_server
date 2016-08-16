# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    ('morethan8', 'morethan8'),
    ('eight888', 'eight888'),
    ('less8', 'less8'),
    ('éyçño', 'éyçño'),
    ('', ''),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result
