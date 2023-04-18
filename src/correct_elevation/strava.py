from __future__ import annotations

from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.correct_elevation.credentials import Credentials
from src.correct_elevation.strava_activity import StravaActivity
from src.strava_API.activities_management.filter_activities import StravaFetcher
from src.strava_API.activities_management.API_request import SummaryOfActivities
from logger.logger import ErrorLogger, InfoLogger
from config import seconds

info_logger = InfoLogger()
error_logger = ErrorLogger()


class Strava:
    driver: WebDriver
    web_driver_wait: WebDriverWait

    def __init__(self, driver: WebDriver):
        driver.get("https://www.strava.com/login")

        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def login(self, credentials: Credentials) -> Strava:
        try:
            email_field = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "email"
                    )
                )
            )
            password_field = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (
                        By.ID,
                        "password"
                    )
                )
            )
            login_button = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "button.btn.btn-primary"
                    )
                )
            )

            email_field.send_keys(credentials.email)
            password_field.send_keys(credentials.password)
            login_button.click()
        except (NoSuchElementException, TimeoutError, Exception) as e:
            error_logger.error(f"Error: {e}")
        finally:
            return self

    def get_latest_activities(self, limit: int = 10) -> List[StravaActivity]:
        try:
            summary_of_activities = SummaryOfActivities()
            strava_fetcher = StravaFetcher(summary_of_activities)
            filtered_activities = strava_fetcher.fetch_activities_summary()
            info_logger.info(filtered_activities)

            return [StravaActivity(self.driver, activity_id) for activity_id in filtered_activities[limit:]]
        except Exception as e:
            error_logger.error(f"Error: {e} in '{__name__}'")
