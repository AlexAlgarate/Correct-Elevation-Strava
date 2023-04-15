from __future__ import annotations

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import seconds


class StravaActivity:
    id: int
    web_driver_wait: WebDriverWait

    def __init__(self, driver: WebDriver, activity_id: int):
        self.id = activity_id

        driver.get(self.get_activity_url())
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def get_activity_url(self) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            A string of the URL of the activity

        """
        return f"https://www.strava.com/activities/{self.id}"

    def is_activity_indoor_cycling(self) -> bool:
        """
        Returns whether the current activity is an indoor cycling activity.

        """
        try:
            indoor_cycling = "spinning"
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

            return indoor_cycling.casefold() in activity_type.casefold()
        except NoSuchElementException:
            return False

    def correct_elevation(self):
        if not self.is_activity_indoor_cycling():
            options_button = self.web_driver_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.app-icon.icon-nav-more"))
            )

            correct_elevation_option = self.web_driver_wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-react-class='CorrectElevation']")
                )
            )

            correct_activity_button = self.web_driver_wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button"
                        # "button.Button--btn--E4CP9.Button--primary--cUgAV"
                    )
                )
            )

            options_button.click()
            correct_elevation_option.click()
            correct_activity_button.click()
