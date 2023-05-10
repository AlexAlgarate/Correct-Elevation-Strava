from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import seconds


class ClickAuthorize:
    """
    Class responsible for clicking on the authorize button in Strava's authentication page.

    Methods:
        - click_authorize(driver: WebDriver) -> bool: uses Selenium to click
        on the authorize button.

    Attributes:
        - driver: WebDriver object used to navigate the web page.
        - web_driver_wait: WebDriverWait object used to wait for
        the authorize button to be clickable.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def click_authorize(self, driver: WebDriver) -> bool:
        """
        Clicks on the authorize button in Strava's authentication page.

        Returns:
            - True if clicks on the button, False otherwise.
        """
        try:
            authorize_button = WebDriverWait(driver, seconds).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button#authorize"
                    )
                )
            )
            authorize_button.click()
            return True
        except NoSuchElementException:
            return False
