import re
from typing import Literal

import pytest

from src.correct_elevation.credentials import Credentials


@pytest.fixture
def valid_credentials() -> Credentials:
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def invalid_email() -> str:
    return "example123example.com"


@pytest.fixture
def empty_credentials() -> Credentials:
    return Credentials("", "")


class TestCredentials:
    def test_valid_credentials_instance(self, valid_credentials: Credentials):
        assert isinstance(valid_credentials, Credentials)

    def test_valid_email_format(
        self,
        valid_credentials: Credentials,
        invalid_email: Literal["example123example.com"],
    ):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        assert re.match(email_regex, valid_credentials.email)
        assert not re.match(email_regex, invalid_email)

    def test_empty_credentials_instance(self, empty_credentials: Credentials):
        assert empty_credentials.email == ""
        assert empty_credentials.password == ""

    def test_null_values(self):
        with pytest.raises(ValueError):
            Credentials(None, None)
