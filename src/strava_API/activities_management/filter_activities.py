from typing import List

import pandas as pd
from pandas import json_normalize

from logger.logger import ErrorLogger

logging_error = ErrorLogger()


class FilterActivities:
    elevation: int
    elevation_column: str
    id: str
    sports: List[str]
    sports_column: str

    def __init__(
        self,
        elevation: int = 0,
        elevation_column: str = "total_elevation_gain",
        id: str = "id",
        sports: List[str] = ["Ride", "Run"],
        sports_column: str = "sport_type"
    ) -> None:
        self.elevation = elevation
        self.elevation_column = elevation_column
        self.id = id
        self.sports = sports
        self.sports_column = sports_column
        self.df = pd.DataFrame()

    def filter_of_activities(self, activities) -> List[int]:
        """
        Returns a list of activity ids that have a sport type of "Ride" and
        "Run" and which total elevation gain was 0 meters.

        Args:
            df : Pandas DataFrame containing activity data.

        Returns:
            List of activity ids

        """
        try:
            self.df = json_normalize(activities)
            filtered_activities = self.df.loc[
                (self.df[self.sports_column].isin(self.sports))
                & (self.df[self.elevation_column] == self.elevation),
                self.id
            ].to_list()
        except Exception as e:
            logging_error.error(f"Error fetching activities from Strava:{e}")
            return []
        if not filtered_activities:
            return []

        return filtered_activities
