from typing import List

import pandas as pd
from pandas import json_normalize

from logger.logger import ErrorLogger
from src.strava_api.get_activities_process.activity_fetcher import ActivityFetcher

logger = ErrorLogger()


class ActivityFilter:
    elevation: int = 0
    elevation_column: str = "total_elevation_gain"
    id: str = "id"
    sports: List[str] = ["Ride", "Run"]
    sports_column: str = "sport_type"
    df: pd.DataFrame
    activities: ActivityFetcher

    def __init__(self) -> None:
        self.activities = ActivityFetcher()

    def filter_activities(self) -> List[int]:
        """
        Filter activities based on the sports type "Ride" and "Run" and
        a total elevation gain of 0 meters.

        Returns:
            List of activity ids

        """
        try:
            self.dataframe = json_normalize(self.activities.get_latest_activities())

            filtered_activities = self.dataframe.loc[
                (self.dataframe[self.sports_column].isin(self.sports))
                & (self.dataframe[self.elevation_column] == self.elevation),
                self.id,
            ].to_list()

        except Exception as e:
            logger.error(f"Error fetching activities from Strava:{e}")
            return []

        if not filtered_activities:
            return []

        return filtered_activities
