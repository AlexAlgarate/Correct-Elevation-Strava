from typing import List

import pandas as pd
from pandas import json_normalize

from config import elevation, elevation_column, id_activity, sports, sports_column
from logger.logger import ErrorLogger
from src.strava_api.get_activities_process.activity_fetcher import ActivityFetcher

logger = ErrorLogger()


class ActivityFilter:
    dataframe: pd.DataFrame
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
                (self.dataframe[sports_column].isin(sports))
                & (self.dataframe[elevation_column] == elevation),
                id_activity,
            ].to_list()

        except Exception as e:
            logger.error(f"Error fetching activities from Strava:{e}")
            return []

        if not filtered_activities:
            return []

        return filtered_activities
