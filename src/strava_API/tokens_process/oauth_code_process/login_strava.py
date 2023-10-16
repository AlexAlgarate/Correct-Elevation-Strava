from __future__ import annotations

from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import exc_log
from utils.config import seconds, url_login_strava

from .credentials import Credentials


class LoginStrava:
    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the LoginStrava object.

        Args:
            driver (WebDriver): The WebDriver object to be used for interacting with the browser.
        """
        self.driver: WebDriver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def open_url(self, url: str) -> None:
        """
        Open the login URL in the browser.
        Args:
            url (str): The URL to be opened.
        """
        self.driver.get(url)

    def find_element(self, function: EC, locator: By, selector: str) -> Any | None:
        """
        Find the element specified by the locator and selector.

        Args:
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.

        Returns:
            The found element or None if not found.
        """
        try:
            element: Any = self.web_driver_wait.until(function((locator, selector)))
            return element
        except NoSuchElementException as e:
            exc_log.exception(e)
            return None

    def fill_field(self, element, value: Credentials) -> None:
        """
        Fill the provided field element with the given value.

        Args:
            element: The field element to be filled.
            value (str): The value to be filled in the field.
        """
        if element:
            element.send_keys(value)

    def click_button(self, element) -> None:
        """
        Click the provided button element.

        Args:
            element: The button element to be clicked.
        """
        if element:
            element.click()

    def login(self) -> None:
        """
        Perform the login process.

        This method opens the login URL, fills in the email and password fields, and clicks the login button.
        """
        try:
            self.open_url(url=url_login_strava)
            self.email_field: Any | None = self.find_element(
                function=EC.visibility_of_element_located,
                locator=By.ID,
                selector="email",
            )
            self.password_field: Any | None = self.find_element(
                function=EC.visibility_of_element_located,
                locator=By.ID,
                selector="password",
            )
            self.login_button: Any | None = self.find_element(
                function=EC.element_to_be_clickable,
                locator=By.CSS_SELECTOR,
                selector="button.btn.btn-primary",
            )

            self.fill_field(element=self.email_field, value=Credentials.email)
            self.fill_field(element=self.password_field, value=Credentials.password)
            self.click_button(element=self.login_button)

        except (TimeoutError, Exception) as e:
            exc_log.exception(f"Error:  {e}")
