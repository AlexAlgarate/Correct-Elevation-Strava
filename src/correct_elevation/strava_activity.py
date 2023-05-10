from __future__ import annotations

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import seconds
from logger.logger import ErrorLogger


error_logger = ErrorLogger()


class StravaActivity:
    id: int
    web_driver_wait: WebDriverWait

    def __init__(self, driver: WebDriver, activity_id: int):
        self.id = activity_id
        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def _get_activity_url(self) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            A string of the URL of the activity

        """
        return f"https://www.strava.com/activities/{self.id}"

    def open_url(self):
        self.driver.get(self._get_activity_url())

    def is_activity_indoor_cycling(self) -> bool:
        """
        Returns whether the current activity is an indoor cycling activity.

        """
        try:
            indoor_activity_type = "spinning"
            header = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h2.text-title3.text-book.marginless")
                )
            )
            activity_type = (
                WebDriverWait(header, seconds)
                .until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
                .text
            )
            return indoor_activity_type.casefold() in activity_type.casefold()
        except NoSuchElementException:
            return False

    def options_button(self) -> bool:
        try:
            options_button = self.web_driver_wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.app-icon.icon-nav-more")
                )
            )
            options_button.click()
            return True
        except Exception:
            return False

    def presence_revert_elevation(self) -> bool:
        try:
            revert_text = "Revertir"
            revert_button = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div[data-react-class='CorrectElevation']",
                    )
                )
            ).text
            return revert_text.casefold() in revert_button.casefold()
        except NoSuchElementException:
            return False

    def correct_button(self) -> bool:
        if not self.presence_revert_elevation():
            try:
                correct_elevation_option = self.web_driver_wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "div[data-react-class='CorrectElevation']")
                    )
                )
                correct_elevation_option.click()
                return True
            except Exception:
                return False
        return True

    def click_correct(self):
        correct_activity_button = self.web_driver_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.Button--primary--cUgAV[type='submit']")
            )
        )
        correct_activity_button.click()

    def correct_elevation(self) -> bool:
        try:
            if self.is_activity_indoor_cycling():
                return False
            self.options_button()
            if self.presence_revert_elevation():
                return False
            self.correct_button()
            self.click_correct()
            return True
        except NoSuchElementException as e:
            error_logger.error(f"Error: {e}")
