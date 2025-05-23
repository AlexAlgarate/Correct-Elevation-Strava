from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.correct_elevation.get_latest_activities import LatestActivities
from src.correct_elevation.strava_activity import StravaActivity
from src.strava_API.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import config, exc_log, inf_log


def setup_driver() -> webdriver.Chrome:
    """
    Initializes a instance of the ChromeDriver class.

    Returns:
        A instance of the ChromeDriver class.
    """
    options = webdriver.ChromeOptions()
    arguments = [
        "--start-maximized",
        "--disable-gpu",
        "--disable-extensions",
    ]
    for args in arguments:
        options.add_argument(args)
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=Service(), options=options)


def proccess_activity(driver: webdriver.Chrome, activity: StravaActivity) -> None:
    """
    Proccess the Strava activity, correct its elevation and create a new instance in the log file.

    Args:
        driver (webdriver.Chrome): webdriver instance
        activity (StravaActivity): id of the activity
    """
    strava_activity = StravaActivity(driver=driver, activity_id=activity.id)
    strava_activity.open_activity_id_url()
    strava_activity.correct_elevation()
    inf_log.info(f"The activity id: {activity.id} has been corrected.")


def main() -> None:
    try:
        with setup_driver() as driver:
            driver.implicitly_wait(time_to_wait=config.seconds)
            login = LoginStrava(driver=driver)
            login.login()
            get_activities = LatestActivities(driver=driver)

            for activity in get_activities.get_latest_activities(
                limit_of_activities=config.limit_of_activities
            ):
                proccess_activity(driver=driver, activity=activity)

    except Exception as e:
        exc_log.exception(e)


if __name__ == "__main__":
    main()
