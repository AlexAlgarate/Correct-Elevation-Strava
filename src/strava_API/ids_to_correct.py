from __future__ import annotations
from typing import Dict, List

import requests

from config import api_url, page_size
from src.strava_API.access_token import GetAccessToken
from logger.logger import ErrorLogger

logger = ErrorLogger()


class GetActivities:
    access_token = GetAccessToken
    """
    Class for getting a summary of all your activities from Strava
    using its API.

    """

    def __init__(self, access_token: GetAccessToken) -> None:
        # self.access_token: str = GetAccessToken().get_strava_access_token()
        self.access_token = access_token

    def _get_activity(self, page: int) -> Dict:
        """
        Makes a GET request to the Strava API for fetching
        activities for a specific page.

        Returns:
            The response from the API in a JSON format.

        """
        try:
            response = requests.get(
                api_url,
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

    def get_all_activities(self) -> List[Dict]:
        """
        Make a GET request to the Strava API for fetching all activities
        by iterating over all available pages in your profile.

        Returns:
            a list of activities in JSON format

        """
        all_activities: List[Dict] = []
        page: int = 1

        while True:
            page_of_activities = self._get_activity(page)

            # Breaks the loop if there are no more activities
            if not page_of_activities:
                break

            all_activities.extend(page_of_activities)
            page += 1

        return all_activities


# def main():

#     # def get_latest_activities(self, limit: int = 10) -> List[StravaActivity]:
#     try:
#         access_token = GetAccessToken().get_strava_access_token()
#         summary_of_activities = GetActivities(access_token)
#         strava_fetcher = StravaFetcher(summary_of_activities).filtered_dataframe()
#         info_logger.info(strava_fetcher)

#         # return [StravaActivity(self.driver, activity_id) for activity_id in filtered_activities[limit:]]
#     except Exception as e:
#         # error_logger.error(f"Error: {e} in '{__name__}'")
#         error_logger.error(f"The error was: {e}")


