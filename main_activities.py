from typing import List

from src.strava_api.activities_management.filter_activities import ActivityFilter


def main(limit: int = 20) -> List[int]:
    strava_activities = ActivityFilter().filter_activities()
    activities = [activity_id for activity_id in strava_activities[:limit]]
    return activities


if __name__ == "__main__":
    activities = main()
    print(activities)
