from typing import List
from src.strava_API.activities_management.filter_activities import \
    FilterActivities
from src.strava_API.activities_management.get_last_activities import \
    GetLastActivities


def main(limit: int = 10) -> List[int]:

    last_activities = GetLastActivities().get_last_activities()
    strava_activities = FilterActivities().filter_of_activities(last_activities)
    activities = [activity_id for activity_id in strava_activities[:limit]]
    return activities


if __name__ == "__main__":
    main()
