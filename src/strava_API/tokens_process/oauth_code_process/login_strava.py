from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import seconds, strava_login_url
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
        # self.credentials = Credentials(EMAIL, PASSWORD)

    def _find_element(self, function: EC, locator: By, selector: str):
        """
        Find the element specified by the locator and selector.

        Args:
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.

        Returns:
            The found element or None if not found.
        """
        try:
            element = self.web_driver_wait.until(function((locator, selector)))
            return element
        except NoSuchElementException:
            return None

    def _open_login_url(self) -> None:
        """
        Open the login URL in the browser.
        """
        return self.driver.get(strava_login_url)

    def _fill_field(self, element, value: Credentials) -> None:
        """
        Fill the provided field element with the given value.

        Args:
            element: The field element to be filled.
            value (str): The value to be filled in the field.
        """
        if element:
            return element.send_keys(value)

    def _click_button(self, element) -> None:
        """
        Click the provided button element.

        Args:
            element: The button element to be clicked.
        """
        if element:
            return element.click()

    def login(self) -> None:
        """
        Perform the login process.

        This method opens the login URL, fills in the email and password fields, and clicks the login button.
        """
        try:
            self._open_login_url()
            email_field = self._find_element(
                EC.visibility_of_element_located, By.ID, "email"
            )
            password_field = self._find_element(
                EC.visibility_of_element_located, By.ID, "password"
            )
            login_button = self._find_element(
                EC.element_to_be_clickable, By.CSS_SELECTOR, "button.btn.btn-primary"
            )

            self._fill_field(email_field, Credentials.email)
            self._fill_field(password_field, Credentials.password)
            self._click_button(login_button)

        except (TimeoutError, Exception) as e:
            ErrorLogger.error(f"Error:  {e}")
