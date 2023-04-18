from typing import Dict, List, Union
from src.strava_API.activities_management.API_request import APIGetRequest


class GetLastActivities:
    get_request: APIGetRequest

    # def __init__(self) -> None:
    #     pass

    def __init__(self) -> None:
        self.get_request = APIGetRequest()

    def get_last_activities(
        self,
        page_size: int = 50
    ) -> List[Dict[str, Union[int, str]]]:
        """
        Make a GET request to the Strava API for fetching
        the last 50 activities.

        Args:
            page_size: Maximum number of activities per page. Default is 50.

        Returns:
            a list of activities in JSON format

        """
        recent_activities = []
        current_page: int = 1

        page_of_activities = self.get_request.get_activity(current_page, page_size)
        recent_activities.extend(page_of_activities)

        return recent_activities
