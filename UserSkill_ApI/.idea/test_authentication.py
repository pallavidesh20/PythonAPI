"""
TDD test cases for user credential verification function to implement basic auth
"""

from settings import USER_NAME, PASSWORD
from authentication import verify

def test_verify_valid():
    assert verify(USER_NAME, PASSWORD) is True


def test_verify_noauth():
    assert verify('', '') is False


def test_verify_invalid_userid():
    assert verify('hello', PASSWORD) is False


def test_verify_invalid_passwd():
    assert verify(USER_NAME, 'hello') is False


