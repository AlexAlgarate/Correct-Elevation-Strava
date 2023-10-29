from typing import Dict, Union

import pytest

from src.strava_api.tokens_process.request_credentials import RequestAccessToken


class MockOauthCodeGetter:
    def get_oauth_code(self) -> str:
        return "test_code"


@pytest.fixture
def request_credentials():
    request_access_token = RequestAccessToken()
    request_access_token.code = MockOauthCodeGetter()
    return request_access_token


class TestGenerateCredentials:
    def test_validate_data_type(self, request_credentials: RequestAccessToken):
        data = request_credentials.get_data_for_request()
        expected_data: Dict[str, Union[str, int]] = {
            "client_id": request_credentials.client_id,
            "client_secret": request_credentials.client_secret,
            "code": "test_code",
            "grant_type": "authorization_code",
        }
        assert data == expected_data
