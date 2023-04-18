from typing import Dict, List, Union
from src.strava_API.activities_management.API_request import APIGetRequest


class GetAllActivities:
    def __init__(self) -> None:
        pass

    def get_all_activities(
        self, max_pages: int = 100
    ) -> List[Dict[str, Union[int, str]]]:
        """
        Make a GET request to the Strava API for fetching all activities
        by iterating over all available pages in your profile.

        Args:
            max_pages: Maximum number of pages to fetch. Default is 100.

        Returns:
            a list of activities in JSON format

        """
        all_activities: List[Dict] = []
        page: int = 1

        while page <= max_pages:
            page_of_activities = self._get_activity_API(page)

            # Breaks the loop if there are no more activities
            if not page_of_activities:
                break

            all_activities.extend(page_of_activities)
            page += 1

        return all_activities
