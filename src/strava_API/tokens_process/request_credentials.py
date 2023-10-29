from typing import Dict, Union

import requests
from dotenv import load_dotenv, set_key
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError, Timeout

from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import (
    OauthCodeGetter,
)
from utils import exc_log
from utils.config import (
    CLIENT_ID,
    SECRET_KEY,
    access_token_env,
    dot_env_file,
    expires_at_env,
    refresh_token_env,
    token_url,
)

load_dotenv()


class RequestAccessToken:
    def __init__(self) -> None:
        self.code = OauthCodeGetter()
        self.client_id: int = CLIENT_ID
        self.client_secret: str = SECRET_KEY
        self.url = token_url

    def get_data_for_request(self) -> Dict[str, Union[str, int]]:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code.get_oauth_code(),
            "grant_type": "authorization_code",
        }
        return data

    def _request_credentials(self) -> Dict[str, Union[str, int]]:
        """
        Send a POST request to the API to get the access token response.

        Returns:
            The access token response as a dictionary.
        Raises:
            requests.RequestException if one of the errors of the dictionary has occurred
        """

        try:
            data: Dict[str, Union[str, int]] = self.get_data_for_request()
            response = requests.post(url=self.url, data=data).json()
            return response

        except (HTTPError, ConnectTimeout, Timeout, ConnectionError) as e:
            exc_log.exception(f"Error: {e}. {type(e)} occurred.")
            raise
        except Exception as e:
            exc_log.exception(f"Error: {e}. {type(e)} occurred.")
            raise

    def _save_credentials_env(self, response: Dict[str, Union[str, int]]) -> None:
        """
        Extract the access token, refresh token, and expires_at from the access token response,
        and store them in an .env file using the set_key function.

        Args:
            response (Dict[str, Union[str, int]]): The access token response as a dictionary.
        """

        access_token: str = response.get("access_token")
        refresh_token: str = response.get("refresh_token")
        expires_at: str = response.get("expires_at")

        set_key(
            dotenv_path=dot_env_file,
            key_to_set=access_token_env,
            value_to_set=access_token,
        )
        set_key(
            dotenv_path=dot_env_file,
            key_to_set=refresh_token_env,
            value_to_set=refresh_token,
        )
        set_key(
            dotenv_path=dot_env_file,
            key_to_set=expires_at_env,
            value_to_set=str(expires_at),
        )

    def generate_access_token(self) -> None:
        """
        Generate and store the Strava access token.

        Raises:
            Exception if an error has occurred
        """
        try:
            response: Dict[str, Union[str, int]] = self._request_credentials()
            self._save_credentials_env(response)

        except Exception as e:
            exc_log.exception(e)
