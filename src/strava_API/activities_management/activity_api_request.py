from __future__ import annotations

from typing import Dict, Union

import requests

from config import api_url
from logger.logger import ErrorLogger
from src.strava_api.tokens_management.access_token import GetAccessToken

logger = ErrorLogger()


class ActivityAPIRequest:
    access_token: GetAccessToken
    url: str

    """
    A class for making GET requests to the Strava API

    """

    def __init__(self, url: str = api_url) -> None:
        """
        Initializes a new instance of the class with a Strava API URL.

        Parameters:
            url (str): The URL of the Strava API.

        """
        self.api_url = url
        self.access_token = GetAccessToken()

    def get_activity(self, page: int = 1, page_size: int = 200) -> Dict[str, Union[int, str]]:
        """
        Makes a GET request to the Strava API for fetching activities for a specific page.
        Max page size available: 200

        Returns:
            The response from the API in a JSON format.

        """
        try:
            response = requests.get(
                self.api_url,
                params={
                    "access_token": self.access_token.get_access_token(),
                    "per_page": page_size,
                    "page": page,
                },
            )

            return response.json()

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error",
            }
            error = error_map.get(type(e), "Other kind of error")
            logger.error(f"Error: {e}. {error} occurred.")
            raise

        except Exception as e:
            logger.error(f"Other error has occurred: {e}")
            raise
