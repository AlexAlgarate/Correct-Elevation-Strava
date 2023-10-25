from typing import Dict, List, Union

from src.strava_api.get_activities_process.activity_api_request import RequestActivities
from utils.config import api_url


class ActivityFetcher:
    api_request: RequestActivities

    def __init__(self) -> None:
        self.api_request = RequestActivities(api_url=api_url)

    def get_latest_activities(self, page_size: int = 100) -> List[Dict[str, Union[int, str]]]:
        """
        Fetches the latest activities by making GET requests to the Strava API.

        Args:
            page_size (int): Maximum number of activities per page. Default is 100.

        Returns:
            List of activities in JSON format

        """
        latest_activities: List[Dict[str, Union[int, str]]] = []
        current_page: int = 1

        page_of_activities: Dict[str, int | str] = self.api_request.get_activity(
            current_page, page_size
        )
        latest_activities.extend(page_of_activities)

        return latest_activities
