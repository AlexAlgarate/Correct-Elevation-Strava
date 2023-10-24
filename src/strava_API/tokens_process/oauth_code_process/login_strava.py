from __future__ import annotations

from typing import Dict

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utils import exc_log
from utils.config import url_login_strava
from utils.locators import login_elements
from utils.web_element_handler import WebElementHandler

from .credentials import Credentials


class LoginStrava:
    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the LoginStrava object.

        Args:
            driver (WebDriver): The WebDriver object to be used for interacting with the browser.
        """
        self.driver: WebDriver = driver
        self.element = WebElementHandler(driver=driver)

    def login(self) -> None:
        """
        Perform the login process.

        This method opens the login URL, fills in the email and password fields, and clicks the login button.
        """
        try:
            self.element.open_url(url=url_login_strava)
            elements: Dict[str, WebElement] = {
                element_name: self.element.find_element(*element_data)
                for element_name, element_data in login_elements.items()
            }
            email_field, password_field, login_button = elements.values()

            self.element.fill_field(element=email_field, value=Credentials.email)
            self.element.fill_field(element=password_field, value=Credentials.password)
            self.element.click_button(element=login_button)

        except (TimeoutError, Exception) as e:
            exc_log.exception(f"Error:  {e}")
