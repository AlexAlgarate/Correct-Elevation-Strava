from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv, set_key

from logger.logger import ErrorLogger
from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import GetOauthCode
from utils.config import (
    CLIENT_ID,
    SECRET_KEY,
    access_token_env,
    dot_env_file,
    expires_at_env,
    refresh_token_env,
    token_url,
)

error_logger = ErrorLogger()

load_dotenv()


class GenerateAccessToken:
    code: GetOauthCode

    def __init__(self) -> None:
        self.code = GetOauthCode()

    def _access_token_post_request(self) -> Dict[str, Union[str, int]]:
        """
        Send a POST request to the API to get the access token response.

        Returns:
            The access token response as a dictionary.
        Raises:
            requests.RequestException if one of the errors of the dictionary has occurred
        """

        try:
            data_to_get_access_token: Dict[str, Any] = {
                "client_id": CLIENT_ID,
                "client_secret": SECRET_KEY,
                "code": self.code.get_oauth_code(),
                "grant_type": "authorization_code",
            }

            response = requests.post(
                url=token_url, data=data_to_get_access_token
            ).json()

            return response

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "ConnectTimeout error",
                requests.exceptions.Timeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error",
            }
            error = error_map.get(type(e), "Other kind of error")
            error_logger.error(f"Error: {e}. {error} occurred.")
            raise

    def _store_access_token_credentials(
        self, response: Dict[str, Union[str, int]]
    ) -> None:
        """
        Extract the access token, refresh token, and expires_at from the access token response,
        and store them in an .env file using the set_key function.

        Args:
            response (Dict[str, Union[str, int]]): The access token response as a dictionary.
        """

        access_token: str = response.get("access_token")
        refresh_token: str = response.get("refresh_token")
        expires_at: str = response.get("expires_at")

        # Set the environment variables
        set_key(dot_env_file, access_token_env, access_token)
        set_key(dot_env_file, refresh_token_env, refresh_token)
        set_key(dot_env_file, expires_at_env, str(expires_at))

    def generate_access_token(self) -> None:
        """
        Generate and store the Strava access token.

        Raises:
            Exception if an error has occurred
        """
        try:
            response: Dict[str, str | int] = self._access_token_post_request()
            self._store_access_token_credentials(response)

        except Exception as e:
            error_logger.error(f"Other kind of error has occurred: {e}")
