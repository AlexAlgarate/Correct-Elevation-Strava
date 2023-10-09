from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.correct_elevation.get_latest_activities import LatestActivities
from src.correct_elevation.strava_activity import StravaActivity
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import exc_log, inf_log
from utils.config import seconds


def main() -> None:
    try:
        service = Service()

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(service=service, options=options) as driver:
            driver.implicitly_wait(seconds)
            login = LoginStrava(driver)
            login.login()
            get_activities = LatestActivities(driver)

            for activity in get_activities.get_latest_activities(limit=3):
                strava_activity = StravaActivity(driver, activity.id)
                strava_activity.open_url()
                strava_activity.correct_elevation()
                inf_log.info(f"The activity id: {activity.id} has been corrected.")
        driver.quit()

    except Exception as e:
        exc_log.exception(e)


if __name__ == "__main__":
    main()
