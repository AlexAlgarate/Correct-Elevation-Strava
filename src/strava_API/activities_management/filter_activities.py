from typing import Dict, List, Union

import pandas as pd
from pandas import json_normalize

from logger.logger import ErrorLogger

logging_error = ErrorLogger()


class FilterActivities:
    elevation: int = 0
    elevation_column: str = "total_elevation_gain"
    id: str = "id"
    sports: List[str] = ["Ride", "Run"]
    sports_column: str = "sport_type"
    df: pd.DataFrame

    def filter_of_activities(self, activities: List[Dict[str, Union[int, str]]]) -> List[int]:
        """
        Filter a given activities object which sports type are "Ride" and
        "Run" and which total elevation gain was 0 meters.

        Args:
            activities : list which contains sports information.

        Returns:
            List of activity ids

        """
        try:
            self.df = json_normalize(activities)

            filtered_activities = self.df.loc[
                (self.df[self.sports_column].isin(self.sports))
                & (self.df[self.elevation_column] == self.elevation),
                self.id,
            ].to_list()

        except Exception as e:
            logging_error.error(f"Error fetching activities from Strava:{e}")
            return []
        if not filtered_activities:
            return []

        return filtered_activities
