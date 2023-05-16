from typing import Dict, List, Union
from src.strava_api.activities_management.activity_api_request import ActivityAPIRequest


class ActivityFetcher:
    api_request: ActivityAPIRequest

    def __init__(self) -> None:
        self.api_request = ActivityAPIRequest()

    def get_latest_activities(
        self, page_size: int = 100
    ) -> List[Dict[str, Union[int, str]]]:
        """
        Use the method request_get_activity() from the module APIGetRequest to make a GET request
        to the Strava API for fetching the latest activities.

        Args:
            page_size: Maximum number of activities per page. Default is 100.

        Returns:
            A list of activities in JSON format

        """
        latest_activities = []
        current_page: int = 1

        page_of_activities = self.api_request.get_activity(current_page, page_size)
        latest_activities.extend(page_of_activities)

        return latest_activities
