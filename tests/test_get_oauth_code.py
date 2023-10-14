import pytest
import os
import sys
from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import GetOauthCode


authorization_url: str = "https://www.strava.com/oauth/authorize"
response_type: str = "response_type=code"
redirect_url: str = "http://localhost/exchange_token"
redirect_uri: str = f"redirect_uri={redirect_url}"
client_id_env: str = "STRAVA_CLIENT_ID"
approval_prompt: str = "approval_prompt=force"
CLIENT_ID: int = int(os.getenv(client_id_env))
client_id: str = f"client_id={CLIENT_ID}"
scopes: str = "read,read_all,activity:read,activity:read_all"
scope: str = f"scope={scopes}"

url_to_get_OAuth_code: str = f"{authorization_url}?{client_id}&{response_type}&{redirect_uri}&{approval_prompt}&{scope}"


class TestOauthCode:
    def setup_method(self) -> str:
        self.oauth_code: str = GetOauthCode().get_oauth_code()
        return self.oauth_code

    def test_code(self) -> None:
        assert self.oauth_code is not None
        assert isinstance(self.oauth_code, str)
        assert len(self.oauth_code) > 0
