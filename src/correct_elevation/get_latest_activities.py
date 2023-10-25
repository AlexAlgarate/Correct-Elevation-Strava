from __future__ import annotations

from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver

from src.correct_elevation.strava_activity import StravaActivity
from src.strava_api.get_activities_process.filter_activities import ActivityFilter
from utils import exc_log


class LatestActivities:
    filter: ActivityFilter

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize a LatestActivities instance.

        Args:
            driver (WebDriver): The WebDriver for browser interaction.
        """

        self.filter = ActivityFilter()
        self.driver: WebDriver = driver

    def get_latest_activities(self, limit: int = 20) -> List[StravaActivity]:
        """
        Get the latest Strava activities.

        Args:
            limit (int): Maximum number of activities to retrieve. Default is 20.

        Returns:
            List[StravaActivity]: A list of StravaActivity instances.
        """

        try:
            filtered_activities: List[int] = self.filter.filter_activities()[:limit]
            return [StravaActivity(self.driver, activity_id) for activity_id in filtered_activities]
        except Exception as e:
            exc_log.exception(e)
