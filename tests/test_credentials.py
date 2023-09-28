# import os
# import sys
from typing import Literal
import re
import pytest

# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, project_root)

# from config import EMAIL, PASSWORD
from src.correct_elevation.credentials import Credentials


@pytest.fixture
def valid_credentials():
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def invalid_email():
    return "example123example.com"


@pytest.fixture
def empty_credentials():
    return Credentials("", "")


def test_valid_credentials_instance(valid_credentials: Credentials):
    assert isinstance(valid_credentials, Credentials)


def test_valid_email_format(
    valid_credentials: Credentials, invalid_email: Literal["example123example.com"]
):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    assert re.match(email_regex, valid_credentials.email)
    assert not re.match(email_regex, invalid_email)


def test_empty_credentials_instance(empty_credentials: Credentials):
    assert empty_credentials.email == ""
    assert empty_credentials.password == ""


def test_null_values():
    with pytest.raises(ValueError):
        Credentials(None, None)
