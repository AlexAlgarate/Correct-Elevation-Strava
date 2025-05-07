import pytest

from src.strava_API.tokens_process.oauth_code_process.credentials import Credentials


@pytest.fixture
def strava_credentials() -> Credentials:
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def invalid_email() -> str:
    return "example123example.com"


@pytest.fixture
def empty_credentials() -> Credentials:
    return Credentials("", "")
