from typing import Dict, List

import pandas as pd
import requests
from pandas import json_normalize

from config import api_url, page_size
from src.utils.access_token import GetAccessToken
from src.utils.logger import ErrorLogger


class SummaryOfActivities:

    """
    Class for getting a summary of all your activities from Strava
    using its API.

    """

    def __init__(self) -> None:
        self.access_token: str = GetAccessToken().get_strava_access_token()
        self.logger = ErrorLogger()

    def _get_activities(self, page: int) -> Dict:
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
            self.logger.error(f"Error: {e}. {error} occurred.")
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
            activities = self._get_activities(page)

            # Breaks the loop if there are no more activities
            if not activities:
                break

            all_activities.extend(activities)
            page += 1

        return all_activities


class StravaFetcher:
    def __init__(self, summary_of_activities: SummaryOfActivities) -> None:
        self.summary_of_activities = summary_of_activities
        self.logger = ErrorLogger()

    @staticmethod
    def filter_activities(df: pd.DataFrame) -> List:
        """
        Returns a list of activity ids that have a sport type of "Ride" and
        "Run" and which total elevation gain was 0 meters.

        Args:
            df : Pandas DataFrame containing activity data.

        Returns:
            List of activity ids

        """
        return df.loc[
            (df["sport_type"].isin(["Ride", "Run"]))
            & (df["total_elevation_gain"] == 0),
            "id"
        ].to_list()

    def fetch_activities_summary(self) -> pd.DataFrame:
        """
        Fetches all activities from Strava and returns a list of activity ids
        that need to be corrected for elevation.

        Returns:
            Pandas DataFrame containing activity summary data

        """
        try:
            activities = self.summary_of_activities.get_all_activities()
        except Exception as e:
            self.logger.error(f"Error fetching activities from Strava API:{e}")
            return pd.DataFrame()
        if not activities:
            self.logger.error("No activities found in Strava account")
            return pd.DataFrame()

        df = json_normalize(activities)
        return self.filter_activities(df)
