from typing import Dict, List, Union
from src.strava_api.activities_management.api_get_request import APIGetRequest


class GetLatestActivities:
    get_request: APIGetRequest

    def __init__(self) -> None:
        self.get_request = APIGetRequest()

    def get_latest_100_activities(self, page_size: int = 100) -> List[Dict[str, Union[int, str]]]:
        """
        Use the method get_activity() from the module api_get_requests to make a GET request
        to the Strava API for fetching the last 100 activities.

        Args:
            page_size: Maximum number of activities per page. Default is 100.

        Returns:
            a list of activities in JSON format

        """
        recent_activities = []
        current_page: int = 1

        page_of_activities = self.get_request.get_activity(current_page, page_size)
        recent_activities.extend(page_of_activities)

        return recent_activities
