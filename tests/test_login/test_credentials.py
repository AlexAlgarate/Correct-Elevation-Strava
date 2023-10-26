import re
from typing import Literal

import pytest

from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials


class TestCredentials:
    def test_valid_credentials_instance(self, strava_credentials: Credentials) -> None:
        assert isinstance(strava_credentials, Credentials)

    def test_valid_email_format(
        self, strava_credentials: Credentials, invalid_email: Literal["example123example.com"]
    ) -> None:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        assert re.match(email_regex, strava_credentials.email)
        assert not re.match(email_regex, invalid_email)

    def test_empty_credentials_instance(self, empty_credentials) -> None:
        assert isinstance(empty_credentials, Credentials)
        assert empty_credentials.email == ""
        assert empty_credentials.password == ""

    def test_raise_ValueError(self) -> None:
        with pytest.raises(ValueError):
            Credentials(email=None, password="password1234")
        with pytest.raises(ValueError):
            Credentials(email="example123@example.com", password=None)
        try:
            Credentials(email="example123@example.com", password="password1234")
        except ValueError:
            pytest.fail("Credentials constructor raised an unexpected exception")
