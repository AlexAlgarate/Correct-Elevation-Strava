from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials
from utils import exc_log
from utils.config import seconds


class DOMElements:
    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the LoginStrava object.

        Args:
            driver (WebDriver): The WebDriver object to be used for interacting with the browser.
        """
        self.driver: WebDriver = driver

    def open_url(self, url: str) -> None:
        """
        Open the login URL in the browser.
        Args:
            url (str): The URL to be opened.
        """
        self.driver.get(url)

    def find_element(
        self, function: EC, locator: By, selector: str
    ) -> WebElement:
        """
        Find the element specified by the locator and selector.

        Args:
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.

        Returns:
            The found element or None if not found.
        """
        try:
            element: WebElement = WebDriverWait(
                driver=self.driver, timeout=seconds
            ).until(function((locator, selector)))
            return element
        except NoSuchElementException as e:
            exc_log.exception(e)
            return None

    def fill_field(self, element: WebElement, value: Credentials) -> None:
        """
        Fill the provided field element with the given value.

        Args:
            element: The field element to be filled.
            value (str): The value to be filled in the field.
        """
        if element:
            element.send_keys(value)

    def click_button(self, element: WebElement) -> None:
        """
        Click the provided button element.

        Args:
            element: The button element to be clicked.
        """
        if element:
            element.click()
