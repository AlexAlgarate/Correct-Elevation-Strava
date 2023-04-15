from src.strava_API.StravaFetcher import StravaFetcher
from src.strava_API.access_token import GetAccessToken
from src.strava_API.ids_to_correct import GetActivities


class GetLastActivities:
    limit = 10
    access_token = GetAccessToken
    activities = GetActivities
    dataframe_of_activities: StravaFetcher

    def __init__(
        self, limit: int,
        access_token: GetAccessToken,
        activities: GetActivities,
        dataframe_of_activities: StravaFetcher
    ) -> None:
        self.limit = limit
        self.activities = activities
        self.access_token = access_token.get_strava_access_token()
        self.dataframe_of_activities = dataframe_of_activities

    def get_last_activities(self):
        pass
