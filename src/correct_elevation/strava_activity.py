from __future__ import annotations

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utils import config, exc_log, locators
from utils.web_element_handler import WebElementHandler


class StravaActivity:
    id: int

    def __init__(self, driver: WebDriver, activity_id: int) -> None:
        """
        Initialize a StravaActivity instance.

        Args:
            driver (WebDriver): The WebDriver for browser interaction.
            activity_id (int): The ID of the Strava activity.
        """

        self.id: int = activity_id
        self.driver: WebDriver = driver
        self.element = WebElementHandler(driver=driver)

    def _get_activity_url(self) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            str: The URL of the activity
        """
        return f"{config.url_strava_activities}{self.id}"

    def open_activity_id_url(self) -> None:
        """
        Open the URL of the Strava activity in the browser.
        """

        self.element.open_url(url=self._get_activity_url())

    def is_activity_indoor_cycling(self) -> bool:
        """
        Returns whether the current activity is an indoor cycling activity.

        Returns:
            bool: True if the activity is indoor cycling, False otherwise.
        """
        try:
            indoor_activity_type: str = "spinning"
            header: WebElement = self.element.find_element(
                *locators.web_elements_correct_elevation["indoor_cycling"]
            )
            activity_type: str = (
                self.element.find_element(
                    *locators.web_elements_correct_elevation["title_header"],
                    element_to_wait_for=header,
                )
            ).text
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
            options_button: WebElement = self.element.find_element(
                *locators.web_elements_correct_elevation["options_button"]
            )
            self.element.click_button(options_button)
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
            revert_text: str = "Revertir"
            revert_button: str = self.element.find_element(
                *locators.web_elements_correct_elevation["revert_button"]
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
                correct_elevation_option: WebElement = self.element.find_element(
                    *locators.web_elements_correct_elevation["correct_button"]
                )
                self.element.click_button(correct_elevation_option)
                return True
            except Exception as e:
                exc_log.exception(e)
                return False
        return True

    def click_correct(self) -> bool:
        """
        Clicks the "Correct elevation" button.
        """

        correct_activity_button: WebElement = self.element.find_element(
            *locators.web_elements_correct_elevation["click_correct_button"]
        )
        self.element.click_button(correct_activity_button)

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
