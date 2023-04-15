from typing import List

import pandas as pd
from pandas import json_normalize

from src.strava_API.ids_to_correct import GetActivities
from logger.logger import ErrorLogger


error_logger = ErrorLogger()


class StravaFetcher:
    activities: GetActivities

    def __init__(self, activities: GetActivities) -> None:
        self.activities = activities

    def _filter_activities(self, df: pd.DataFrame) -> List:
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

    def filtered_dataframe(self) -> pd.DataFrame:
        """
        Fetches all activities from Strava and returns a list of activity ids
        that need to be corrected for elevation.
        Returns:
            Pandas DataFrame containing activity summary data
        """
        try:
            activities = self.activities.get_all_activities()
        except Exception as e:
            self.logger.error(f"Error fetching activities from Strava API:{e}")
            return pd.DataFrame()
        if not activities:
            error_logger.error("No activities found in Strava account")
            return pd.DataFrame()

        df = json_normalize(activities)
        return self._filter_activities(df)
