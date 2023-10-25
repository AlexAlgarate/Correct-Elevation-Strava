from __future__ import annotations
from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials
from utils import exc_log
from utils.config import seconds


class WebElementHandler:
    """
    A class for handling web elements using Selenium WebDriver.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the WebElementHandler object.

        Args:
            driver (WebDriver): The WebDriver object to interact with the browser.
        """
        self.driver: WebDriver = driver

    def open_url(self, url: str) -> None:
        """
        Open the specified URL in the browser.

        Args:
            url (str): The URL to be opened.
        """
        self.driver.get(url)

    def find_element(
        self, condition: EC, locator: By, selector: str, element_to_wait_for: Any = None
    ) -> WebElement:
        """
        Find the element specified by the locator and selector.

        Args:
            condition (EC): The expected condition to wait for.
            locator (By): The method used to locate the element.
            selector (str): The value used to locate the element.
            element_to_wait_for (Any): The element to wait for load the DOM
        Returns:
            The found element or None if not found.
        """
        try:
            if element_to_wait_for:
                element: WebElement = WebDriverWait(
                    driver=element_to_wait_for, timeout=seconds
                ).until(condition((locator, selector)))
            else:
                element: WebElement = WebDriverWait(driver=self.driver, timeout=seconds).until(
                    condition((locator, selector))
                )
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
