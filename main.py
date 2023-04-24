from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import EMAIL, PASSWORD, seconds
from logger.logger import ErrorLogger, InfoLogger
from src.correct_elevation.credentials import Credentials
from src.correct_elevation.strava import Strava
from src.correct_elevation.strava_activity import StravaActivity

info_logger = InfoLogger()
error_logger = ErrorLogger()


def main():
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as driver:
            driver.implicitly_wait(seconds)

            credentials = Credentials(EMAIL, PASSWORD)
            strava = Strava(driver)

            for activity in strava.login(credentials).get_latest_activities(limit=2):
                strava_activity = StravaActivity(driver, activity.id)
                strava_activity.correct_elevation()

        driver.quit()

    except Exception as e:
        error_logger.error(f"Error: {e} in '{__name__}'")


if __name__ == "__main__":
    main()
