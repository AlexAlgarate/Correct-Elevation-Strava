from time import time
from typing import Dict, Optional, Tuple, Union

import requests
from dotenv import load_dotenv, set_key
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError, Timeout

from utils import exc_log
from utils.config import (
    EXPIRES_AT,
    access_token_env,
    dot_env_file,
    expires_at_env,
    refresh_data,
    refresh_token_env,
    token_url,
)


class RefreshTokenManager:
    load_dotenv()
    """
    A class to manage the refreshing proccess of the access token.
    If the access token has expired, it makes a POST request to the Strava API
    using the refresh token and store the new credentials in the .env file.
    """

    def __init__(self) -> None:
        self.current_time: int = int(time())

    def _check_expired(self) -> bool:
        """
        Returns True if the expiration date of the access token is less than
        the current time.
        Returns False otherwise.
        """

        try:
            expires_at: int = int(EXPIRES_AT)
            if expires_at < self.current_time:
                print("The access token has expired.")
            return expires_at < self.current_time

        except ValueError as e:
            exc_log.exception(f"Error while parsing EXPIRES_AT value: {e}")
            raise ValueError("EXPIRES_AT value is not a valid integer timestamp")

        except TypeError as e:
            exc_log.exception(f"Error while parsing EXPIRES_AT value: {e}")
            raise TypeError("EXPIRES_AT has to be an integer, not a string")

        except Exception as e:
            exc_log.exception(f"An unexpected error occurred: {e}")
            raise

    def _update_env(
        self, access_token: str, refresh_token: str, expires_at: Optional[int]
    ) -> None:
        """
        Update the access token and expires_at in the .env file.

        Args:
            - access_token (str): the string of the refreshed access token
            - refresh_token (str): the string of the refresehd refresh token
            - expires_at (Optional[int]): the new expiration timestampt of the access token
        """

        try:
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
            if expires_at is not None:
                set_key(
                    dotenv_path=dot_env_file,
                    key_to_set=expires_at_env,
                    value_to_set=str(expires_at),
                )

        except FileNotFoundError as e:
            exc_log.exception(f"Could not find the .env file: {e}")
        except KeyError as e:
            exc_log.exception(f"Key error while updating the .env: {e}")
        except Exception as e:
            exc_log.exception(f"Error while updating the .env: {e}")

    def _request_refresh_token(
        self, params: Dict[str, Union[str, int]]
    ) -> requests.Response:
        """
        Make a POST request to the token URL using the provided refresh data.

        Args:
            params (Dict[str, Union[str, int]]): The data for the refresh request.

        Returns:
            requests.Response: The response object.
        """
        return requests.post(url=token_url, data=params)

    def _parse_refresh_request(
        self, refresh_response: requests.Response
    ) -> Dict[str, Union[str, int]]:
        """
        Parse the refresh response JSON data.

        Args:
            refresh_response (requests.Response): The response object.

        Returns:
            Dict[str, Union[str, int]]: The parsed response data.
        """
        refresh_response.raise_for_status()
        data = refresh_response.json()

        for key in ("access_token", "refresh_token", "expires_at"):
            if key not in data:
                raise ValueError("Missing key in response data: " + key)
        return data

    def _extract_credentials(self, data: Dict[str, Union[str, int]]) -> Tuple[str, int]:
        """
           Extract the access token, refresh token, and expiration time from the response data.

        Args:
            data (Dict[str, Union[str, int]]): The parsed response data.

        Returns:
            Tuple[str, int]: A tuple containing the access token, refresh token and expiration time.
        """

        access_token: str = data.get("access_token")
        refresh_token: str = data.get("refresh_token")
        expires_at: int = int(data.get("expires_at"))

        return access_token, refresh_token, expires_at

    def refresh_access_token(self) -> str:
        """
        Refresh the access token using the refresh token and update the credentials in .env file.

        Returns:
            str: The refreshed access token.

        Raises:
            requests.RequestException: If an error occurs during the request.
        """

        try:
            params: Dict[str, str | int] = refresh_data
            request: requests.Response = self._request_refresh_token(params)
            response: Dict[str, str | int] = self._parse_refresh_request(request)
            access_token, refresh_token, expires_at = self._extract_credentials(
                response
            )
            self._update_env(access_token, refresh_token, expires_at)
            return access_token

        except (HTTPError, ConnectTimeout, Timeout, ConnectionError) as e:
            exc_log.exception(f"Error: {e}. {type(e)} occurred.")
            raise
        except Exception as e:
            exc_log.exception(f"Error: {e}. {type(e)} occurred.")
            raise
