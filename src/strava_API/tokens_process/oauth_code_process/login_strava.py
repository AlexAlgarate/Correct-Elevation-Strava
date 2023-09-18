from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import EMAIL, PASSWORD, seconds, strava_login_url
from logger.logger import ErrorLogger
from src.correct_elevation.credentials import Credentials


class LoginStrava:
    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the LoginStrava object.

        Args:
            driver (WebDriver): The WebDriver object to be used for interacting with the browser.
        """
        self.driver: WebDriver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)
        self.credentials = Credentials(EMAIL, PASSWORD)

    def _open_login_url(self) -> None:
        """
        Open the login URL in the browser.
        """
        return self.driver.get(strava_login_url)

    def _fill_fields(self, locator: By, selector: str) -> None:
        """
        Find the element specified by the locator and selector and fill it with the provided value.

        Args:
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.

        Returns:
            The filled field element.
        """
        field = self.web_driver_wait.until(
            EC.visibility_of_element_located((locator, selector))
        )
        return field

    def _click_button(self, locator: By, selector: str) -> None:
        """
        Find the element specified by the locator and selector and click it.

        Args:
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.
        """
        button = self.web_driver_wait.until(
            EC.element_to_be_clickable((locator, selector))
        )
        return button.click()

    def login(self) -> None:
        """
        Perform the login process.

        This method opens the login URL, fills in the email and password fields, and clicks the login button.
        """
        try:
            self._open_login_url()
            email = self._fill_fields(By.ID, "email")
            email.send_keys(self.credentials.email)
            password = self._fill_fields(By.ID, "password")
            password.send_keys(self.credentials.password)
            self._click_button(By.CSS_SELECTOR, "button.btn.btn-primary")

        except (NoSuchElementException, TimeoutError) as e:
            ErrorLogger.error(f"Error:  {e}")
