from __future__ import annotations

from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver

from logger.logger import ErrorLogger
from src.correct_elevation.strava_activity import StravaActivity
from src.strava_api.get_activities_process.filter_activities import ActivityFilter

logger = ErrorLogger()


class LatestActivities:
    filter: ActivityFilter

    def __init__(self, driver: WebDriver) -> None:
        self.filter = ActivityFilter()
        self.driver: WebDriver = driver

    def get_latest_activities(self, limit: int = 20) -> List[StravaActivity]:
        try:
            filtered_activities: List[int] = self.filter.filter_activities()[:limit]
            return [
                StravaActivity(self.driver, activity_id)
                for activity_id in filtered_activities
            ]
        except Exception as e:
            logger.error(f"An error has occurred: {e}")
