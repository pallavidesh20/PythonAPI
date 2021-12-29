"""
The start point of pytest where we create the fixture that creates a flask client object
that is used to send the CRUD requests.
"""

import pytest
from base64 import b64encode
from settings import DATABASE_URL_TEST
from app import create_app
from settings import USER_NAME, PASSWORD
from contantsTDD import INVALID_USER, INVALID_PWD


@pytest.fixture
def client():
    app = create_app(DATABASE_URL_TEST)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_auth():
    cred_string = USER_NAME + ':' + PASSWORD
    cred_bytes = cred_string.encode("utf-8")
    return b64encode(cred_bytes).decode("utf-8")


@pytest.fixture
def invalid_password():
    cred_string = USER_NAME + ':' + INVALID_PWD
    cred_bytes = cred_string.encode("utf-8")
    return b64encode(cred_bytes).decode("utf-8")


@pytest.fixture
def invalid_user():
    cred_string = INVALID_USER + ':' + PASSWORD
    cred_bytes = cred_string.encode("utf-8")
    return b64encode(cred_bytes).decode("utf-8")

