# -*- coding: utf-8 -*-
import pytest
import client

MSG_TABLE = [
    ('morethan8', 'morethan8'),
    ('eight888', 'eight888'),
    ('less8', 'less8'),
    ('éyçño', u'éyçño'),
    ('', ''),
]
STRING_TABLE = [
    ('rodstewartisagreatsinger'),
    (b'alsdkfj;sahgaeofljds;lghaksjfeijafghdlsfj'),
    ('éyçño'),
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_send_msg(msg, result):
    """Test to see that message sent is returned"""
    assert client.send_msg(msg) == result


@pytest.mark.parametrize('a_string', STRING_TABLE)
def test_force_unicode(a_string):
    """Test type is forced to unicode"""
    assert type(client.force_unicode(a_string)) is type(u'')


def test_main():
    """Test main cal without message exits system"""
    with pytest.raises(SystemExit):
        client.main()
