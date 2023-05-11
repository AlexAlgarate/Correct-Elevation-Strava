import time
from typing import Dict, Optional, Tuple, Union

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


error_logger = ErrorLogger()


class RefreshTokenManager:

    """
    A class to manage the refreshing proccess of the access token.
    THis class is used by otheer files to check if the access token
    has expired and refresh it by making a POST request to the Strava API
    using a refresh token.
    The new credentials are saved in the .env file.

    """

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
            error_logger.error("EXPIRES_AT value should be an integer")
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
            error_logger.error(f"Could not find the .env file: {e}")
        except KeyError as e:
            error_logger.error(f"Key error while updating the .env: {e}")
        except Exception as e:
            error_logger.error(f"Error while updating the .env: {e}")

    def _make_refresh_post_request(
        self, params: Dict[str, Union[str, int]]
    ) -> requests.Response:
        """
        Make a POST request to the token URL using the provided refresh data.

        Args:
            params: The data for the refresh request.

        Returns:
            The response object.
        """
        return requests.post(url=token_url, data=params)

    def _parse_refresh_request(
        self, refresh_response: requests.Response
    ) -> Dict[str, Union[str, int]]:
        """
        Parse the refresh response JSON data.

        Args:
            refresh_response: The response object.

        Returns:
            The parsed response data.
        """
        refresh_response.raise_for_status()
        refresh_response_data = refresh_response.json()
        for key in ("access_token", "refresh_token", "expires_at"):
            if key not in refresh_response_data:
                raise ValueError("Missing key in response data: " + key)
        return refresh_response_data

    def _extract_credentials(
        self, refresh_response_data: Dict[str, Union[str, int]]
    ) -> Tuple[str, str, int]:
        """
           Extract the access token, refresh token, and expiration time from the response data.

        Args:
            refresh_response_data: The parsed response data.

        Returns:
            A tuple containing the access token, refresh token, and expiration time.
        """

        access_token: str = refresh_response_data.get("access_token")
        refresh_token: str = refresh_response_data.get("refresh_token")
        expires_at: int = int(refresh_response_data.get("expires_at"))

        return access_token, refresh_token, expires_at

    def refresh_access_token(self):
        try:
            params = refresh_data
            request_to_refresh_token = self._make_refresh_post_request(params)
            response_from_request = self._parse_refresh_request(
                request_to_refresh_token
            )
            access_token, refresh_token, expires_at = self._extract_credentials(
                response_from_request
            )
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
            error_logger.error(f"Error: {e}. {error} occurred.")
            raise
