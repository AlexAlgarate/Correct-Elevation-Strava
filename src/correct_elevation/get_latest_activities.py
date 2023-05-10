from __future__ import annotations

from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver
from src.correct_elevation.strava_activity import StravaActivity
from src.strava_api.activities_management.filter_activities import FilterActivities
from src.strava_api.activities_management.get_last_activities import GetLastActivities
from logger.logger import ErrorLogger

error_logger = ErrorLogger()


class GetLatestActivities:
    filter: FilterActivities
    get_activities: GetLastActivities

    def __init__(self, driver: WebDriver) -> None:
        self.filter = FilterActivities()
        self.get_activities = GetLastActivities()
        self.driver = driver

    def get_latest_activities(self, limit: int = 20) -> List[StravaActivity]:
        api_activities = self.get_activities.get_last_activities()
        filtered_activities = self.filter.filter_of_activities(api_activities)[:limit]
        return [
            StravaActivity(self.driver, activity_id)
            for activity_id in filtered_activities
        ]
