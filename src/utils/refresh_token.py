import time
from typing import Dict, Optional, Union

import requests
from dotenv import set_key

from config import (CLIENT_ID, EXPIRES_AT, REFRESH_TOKEN, SECRET_KEY,
                    access_token_env, dot_env_file, expires_at_env,
                    refresh_token_env, refresh_token_grant_type, token_url)
# from src.utils.generate_credentials import GenerateAccessToken
from src.utils.logger import ErrorLogger


class RefreshTokenManager:

    """
    A class to manage the refreshing proccess of the access token.
    THis class is used by otheer files to check if the access token
    has expired and refresh it by making a POST request to the Strava API
    using a refresh token.
    The new credentials are saved in the .env file.

    """

    def __init__(self) -> None:
        self.logger = ErrorLogger()

    def _check_expired(self) -> bool:

        """
        Returns True if the expiration date of the access token is less than
        the current time.
        Returns False otherwise.

        """
        expires_at_str = EXPIRES_AT
        if expires_at_str is None:
            return False

        try:
            expires_at = int(expires_at_str)

        except ValueError:
            self.logger.error("EXPIRES_AT value should be an integer")
            return False

        current_time = int(time.time())
        return expires_at < current_time

    def _update_env(
        self,
        access_token: str,
        refresh_token: str,
        expires_at: Optional[int]
    ) -> None:

        """
        Update the access token and expires_at in the .env file.

        """

        try:
            set_key(dot_env_file, access_token_env, access_token)
            set_key(dot_env_file, refresh_token_env, refresh_token)
            if expires_at is not None:
                set_key(dot_env_file, expires_at_env, str(expires_at))

        except FileNotFoundError as e:
            self.logger.error(f"Could not find the .env file: {e}")
        except KeyError as e:
            self.logger.error(f"Key error while updating the .env: {e}")
        except Exception as e:
            self.logger.error(f"Error while updating the .env: {e}")

    def _refresh_access_token(self) -> str:

        """
        Refresh the access token by making a POST request to the API and
        saves the new credentials in the .env file.

        Return:
            The new access token

        """

        refresh_data: Dict[str, Union[str, int]] = {
            "client_id": CLIENT_ID,
            "client_secret": SECRET_KEY,
            "grant_type": refresh_token_grant_type,
            "refresh_token": REFRESH_TOKEN
        }
        try:
            refresh_response = requests.post(
                url=token_url,
                data=refresh_data
            )

            refresh_response.raise_for_status()
            refresh_response_data = refresh_response.json()

            for key in ("access_token", "refresh_token", "expires_at"):
                if key not in refresh_response_data:
                    raise ValueError("Missing key in response data: " + key)

            access_token: str = refresh_response_data["access_token"]
            refresh_token: str = refresh_response_data["refresh_token"]
            expires_at: int = int(refresh_response_data["expires_at"])

            self._update_env(access_token, refresh_token, expires_at)

            return access_token

        except (
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError
        ) as e:
            self.logger.error(f"Error while making the request to the API:{e}")
            raise
            # new_credentials = GenerateAccessToken()
            # new_credentials.generate_access_token()
