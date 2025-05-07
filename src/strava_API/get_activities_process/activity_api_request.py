from typing import Dict, Union

import requests

from src.strava_API.tokens_process.get_access_token import GetAccessToken
from utils import exc_log


class RequestActivities:
    access_token: GetAccessToken
    url: str

    """
    A class for making GET requests to the Strava API

    """

    def __init__(self, api_url: str) -> None:
        """
        Initializes a new instance of the class with a Strava API URL.

        Parameters:
            url (str): The URL of the Strava API.

        """
        self.api_url: str = api_url
        self.access_token = GetAccessToken()

    def get_activity(
        self, page: int = 1, page_size: int = 200
    ) -> Dict[str, Union[int, str]]:
        """
        Makes a GET request to the Strava API for fetching activities for a specific page.
        Max page size available: 200

        Args:
            page (int): The page number.
            page_size (int): The number of activities per page.

        Returns:
            The response from the API in a JSON format.

        """
        try:
            params: Dict[str, Union[int, str]] = {
                "access_token": self.access_token.get_access_token(),
                "per_page": page_size,
                "page": page,
            }
            response: requests.Response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            exc_log.exception(f"Error: {e}")
            raise
