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
        driver.get(self._get_activity_url())
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def _get_activity_url(self) -> str:
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
            activity_type = WebDriverWait(header, seconds).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "title"
                    )
                )
            ).text

            return indoor_cycling.casefold() in activity_type.casefold()
        except NoSuchElementException:
            return False

    def options_button(self):
        options_button = self.web_driver_wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.app-icon.icon-nav-more"
                        )
                    )
                )
        options_button.click()

    def correct_button(self):
        correct_elevation_option = self.web_driver_wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[data-react-class='CorrectElevation']"
                )
            )
        )
        correct_elevation_option.click()

    def click_correct(self):
        correct_activity_button = self.web_driver_wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button"
                )
            )
        )
        correct_activity_button.click()

    def correct_elevation_strava(self):
        if not self.is_activity_indoor_cycling:
            self.options_button()
            self.correct_button()
            self.click_correct()

    def correct_elevation(self):
        try:
            if not self.is_activity_indoor_cycling():
                options_button = self.web_driver_wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.app-icon.icon-nav-more"
                        )
                    )
                )

                correct_elevation_option = self.web_driver_wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div[data-react-class='CorrectElevation']"
                        )
                    )
                )

                correct_activity_button = self.web_driver_wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button"
                        )
                    )
                )

                options_button.click()
                print("Clicked options button")
                correct_elevation_option.click()
                print("Clicked correct button")
                correct_activity_button.click()
                print("Clicked ACCEPT button")
        except NoSuchElementException as e:
            print(e)
        finally:
            return self
