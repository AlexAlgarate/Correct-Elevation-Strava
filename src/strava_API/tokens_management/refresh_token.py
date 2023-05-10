import time
from typing import Optional

import requests
from dotenv import set_key

from config import (
    EXPIRES_AT,
    access_token_env,
    dot_env_file,
    expires_at_env,
    refresh_data,
    refresh_token_env,
    token_url,
)
from logger.logger import ErrorLogger


class RefreshTokenManager:
    error_logger: ErrorLogger

    """
    A class to manage the refreshing proccess of the access token.
    THis class is used by otheer files to check if the access token
    has expired and refresh it by making a POST request to the Strava API
    using a refresh token.
    The new credentials are saved in the .env file.

    """

    def __init__(self) -> None:
        self.error_logger = ErrorLogger()

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
            self.error_logger.error("EXPIRES_AT value should be an integer")
            return False

        current_time = int(time.time())
        return expires_at < current_time

    def _update_env(
        self, access_token: str, refresh_token: str, expires_at: Optional[int]
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
            self.error_logger.error(f"Could not find the .env file: {e}")
        except KeyError as e:
            self.error_logger.error(f"Key error while updating the .env: {e}")
        except Exception as e:
            self.error_logger.error(f"Error while updating the .env: {e}")

    def _refresh_access_token(self) -> str:
        """
        Refresh the access token by making a POST request to the API and
        saves the new credentials in the .env file.

        Return:
            The new access token

        """

        try:
            refresh_response = requests.post(url=token_url, data=refresh_data)

            refresh_response.raise_for_status()
            refresh_response_data = refresh_response.json()

            for key in ("access_token", "refresh_token", "expires_at"):
                if key not in refresh_response_data:
                    raise ValueError(f"Missing key in response data: {key}")

            access_token: str = refresh_response_data.get("access_token")
            refresh_token: str = refresh_response_data.get("refresh_token")
            expires_at: int = int(refresh_response_data.get("expires_at"))

            self._update_env(access_token, refresh_token, expires_at)
            return access_token

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "Timeout error",
                requests.exceptions.Timeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error",
            }
            error = error_map.get(type(e), "Other kind of error")
            self.error_logger.error(f"Error: {e}. {error} occurred.")
            raise
