from __future__ import annotations
from typing import Any

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import exc_log
from utils.config import seconds


class StravaActivity:
    id: int
    web_driver_wait: WebDriverWait

    def __init__(self, driver: WebDriver, activity_id: int) -> None:
        """
        Initialize a StravaActivity instance.

        Args:
            driver (WebDriver): The WebDriver for browser interaction.
            activity_id (int): The ID of the Strava activity.
        """

        self.id = activity_id
        self.driver: WebDriver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def _get_activity_url(self) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            str: The URL of the activity
        """

        return f"https://www.strava.com/activities/{self.id}"

    def open_url(self) -> None:
        """
        Open the URL of the Strava activity in the browser.
        """

        self.driver.get(self._get_activity_url())

    def is_activity_indoor_cycling(self) -> bool:
        """
        Returns whether the current activity is an indoor cycling activity.

        Returns:
            bool: True if the activity is indoor cycling, False otherwise.
        """
        try:
            indoor_activity_type = "spinning"
            header: Any = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h2.text-title3.text-book.marginless")
                )
            )
            activity_type: Any = (
                WebDriverWait(header, seconds)
                .until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
                .text
            )
            return indoor_activity_type.casefold() in activity_type.casefold()
        except (NoSuchElementException, Exception) as e:
            exc_log.exception(e)
            return False

    def options_button(self) -> bool:
        """
        Clicks the options button on the Strava activity page.

        Returns:
            bool: True if the options button was successfully clicked, False otherwise.
        """

        try:
            options_button: Any = self.web_driver_wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.app-icon.icon-nav-more")
                )
            )
            options_button.click()
            return True
        except (NoSuchElementException, Exception) as e:
            exc_log.exception(e)
            return False

    def presence_revert_elevation(self) -> bool:
        """
        Checks if the "Revert" button is present on the page.

        Returns:
            bool: True if the "Revert" button is present, False otherwise.
        """
        try:
            revert_text = "Revertir"
            revert_button: Any = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div[data-react-class='CorrectElevation']",
                    )
                )
            ).text
            return revert_text.casefold() in revert_button.casefold()
        except NoSuchElementException as e:
            exc_log.exception(e)
            return False

    def correct_button(self) -> bool:
        """
        Clicks the correct elevation button on the Strava activity page.

        Returns:
            bool: True if the correct elevation button was
            successfully clicked, False otherwise.
        """
        if not self.presence_revert_elevation():
            try:
                correct_elevation_option: Any = self.web_driver_wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "div[data-react-class='CorrectElevation']")
                    )
                )
                correct_elevation_option.click()
                return True
            except Exception as e:
                exc_log.exception(e)
                return False
        return True

    def click_correct(self) -> bool:
        """
        Clicks the "Correct" button to apply elevation
        correction on the Strava activity page.
        """
        correct_activity_button: Any = self.web_driver_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.Button--primary--cUgAV[type='submit']")
            )
        )
        correct_activity_button.click()

    def correct_elevation(self) -> bool:
        """
        Corrects the elevation of the Strava activity.

        Returns:
            bool: True if the elevation correction was successful,
            False otherwise.
        """
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
            exc_log.exception(e)
