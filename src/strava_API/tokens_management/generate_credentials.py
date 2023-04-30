from typing import Dict, Union

import requests
from dotenv import load_dotenv, set_key

from config import (
    CLIENT_ID,
    SECRET_KEY,
    access_token_env,
    dot_env_file,
    expires_at_env,
    refresh_token_env,
    token_url
)
from src.strava_API.tokens_management.get_oauth_code import GetOAuthCode
from logger.logger import ErrorLogger

error_logger = ErrorLogger()

load_dotenv()


class GenerateAccessToken:
    code: GetOAuthCode

    def __init__(self) -> None:
        self.code = GetOAuthCode()

    def generate_access_token(self) -> None:
        """
        Get the credentials (access_token, refresh_token, and expires_at)
        from by making a POST request to the API.
        Finally, these credentials are stored in an .env file
        using the set_key function.

        """
        try:
            data_to_get_access_token: Dict[str, Union[str, int]] = {
                "client_id": CLIENT_ID,
                "client_secret": SECRET_KEY,
                "code": self.code.get_oauth_code(),
                "grant_type": "authorization_code"
            }

            response = requests.post(
                url=token_url, data=data_to_get_access_token
            ).json()

            access_token: str = response.get("access_token")
            refresh_token: str = response.get("refresh_token")
            expires_at: str = response.get("expires_at")

            # Set the environment variables
            set_key(dot_env_file, access_token_env, access_token)
            set_key(dot_env_file, refresh_token_env, refresh_token)
            set_key(dot_env_file, expires_at_env, str(expires_at))

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "Timeout error",
                requests.exceptions.Timeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error"
            }
            error = error_map.get(type(e), "Other kind of error")
            error_logger.error(f"Error: {e}. {error} occurred.")
            raise

        except Exception as e:
            error_logger.error(f"Other kind of error has occurred: {e}")
