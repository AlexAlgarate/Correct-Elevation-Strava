from typing import List

from src.strava_api.activities_management.filter_activities import FilterActivities

# from src.strava_api.activities_management.get_last_activities import \
#     GetLastActivities
from src.strava_api.activities_management.get_all_activities import GetAllActivities


def main(limit: int = 20) -> List[int]:
    all_activities = GetAllActivities().get_all_activities()
    strava_activities = FilterActivities().filter_of_activities(all_activities)
    activities = [activity_id for activity_id in strava_activities[:limit]]
    return activities
    # last_activities = GetLastActivities().get_last_activities()
    # strava_activities = FilterActivities().filter_of_activities(last_activities)
    # activities = [activity_id for activity_id in strava_activities[:limit]]
    # return activities


if __name__ == "__main__":
    activities = main()
    print(activities)
