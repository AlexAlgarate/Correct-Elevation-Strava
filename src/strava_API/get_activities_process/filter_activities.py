from typing import List

import pandas as pd
from pandas import json_normalize

from src.strava_api.get_activities_process.activity_fetcher import ActivityFetcher
from utils import exc_log


class ActivityFilter:
    dataframe: pd.DataFrame
    activities: ActivityFetcher

    def __init__(self) -> None:
        self.activities = ActivityFetcher()

    def filter_activities(
        self,
        columns_sport: str,
        sports: List[str],
        elevation_column: str,
        meters_elevation: int,
        id_actvity: str,
    ) -> List[int]:
        """
        Filter activities based on the sports type "Ride" and "Run" and
        a total elevation gain of 0 meters.

        Returns:
            List of activity ids

        """
        try:
            self.dataframe = json_normalize(self.activities.get_latest_activities())

            filtered_activities: List[int] = self.dataframe.loc[
                (self.dataframe[columns_sport].isin(sports))
                & (self.dataframe[elevation_column] == meters_elevation),
                id_actvity,
            ].to_list()

        except Exception as e:
            exc_log.exception(f"Error fetching activities from Strava:{e}")
            return []

        if not filtered_activities:
            return []

        return filtered_activities
