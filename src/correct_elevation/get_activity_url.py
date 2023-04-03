class GetACtivityURL:
    @staticmethod
    def get_activity_url(activity_id: int) -> str:

        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            A string of the URL of the activity

        """
        return f"https://www.strava.com/activities/{activity_id}"
