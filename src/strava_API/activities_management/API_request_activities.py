from __future__ import annotations

from typing import Dict, List, Union

import requests

from config import api_url
from logger.logger import ErrorLogger
from src.strava_API.tokens_management.access_token import GetAccessToken

logger = ErrorLogger()


class APIRequesting:
    access_token: str
    url: str

    """
    A class fro fetching activities from Strava API

    """

    def __init__(
        self,
        access_token: GetAccessToken,
        url: str = api_url
    ) -> None:
        """
            Initializes a new instance of the class with a Strava access token.

            Parameters:
                access_token (GetAccessToken): The Strava access token.

        """
        self.access_token = access_token
        self.api_url = url

    def _get_activity_API(
        self,
        page: int = 1,
        page_size: int = 200
    ) -> Dict[str, Union[int, str]]:
        """
        Makes a GET request to the Strava API for fetching
        activities for a specific page.

        Returns:
            The response from the API in a JSON format.

        """
        try:
            response = requests.get(
                self.api_url,
                params={
                    "access_token": self.access_token,
                    "per_page": page_size,
                    "page": page
                }
            )
            # Raises an exception if there was a HTTP error in the reques
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error"
            }
            error = error_map.get(type(e), "Other kind of error")
            logger.error(f"Error: {e}. {error} occurred.")
            raise

        except Exception as e:
            logger.error(f"Other error has occurred: {e}")
            raise

    def get_all_activities(self, max_pages: int = 100) -> List[Dict]:
        """
        Make a GET request to the Strava API for fetching all activities
        by iterating over all available pages in your profile.

        Args:
            max_pages: Maximum number of pages to fetch. Default is 100.

        Returns:
            a list of activities in JSON format

        """
        all_activities: List[Dict] = []
        page: int = 1

        while page <= max_pages:
            page_of_activities = self._get_activity_API(page)

            # Breaks the loop if there are no more activities
            if not page_of_activities:
                break

            all_activities.extend(page_of_activities)
            page += 1

        return all_activities

    def get_last_100_activities(self, page_size: int = 50) -> List[Dict]:
        """
        Make a GET request to the Strava API for fetching
        the last 50 activities.

        Args:
            page_size: Maximum number of activities per page. Default is 50.

        Returns:
            a list of activities in JSON format

        """
        recent_activities: List[Dict] = []
        current_page: int = 1

        page_of_activities = self._get_activity_API(current_page, page_size)
        recent_activities.extend(page_of_activities)

        return recent_activities
