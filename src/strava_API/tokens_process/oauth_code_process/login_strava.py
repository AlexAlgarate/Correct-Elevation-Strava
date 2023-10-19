from __future__ import annotations

from typing import List, Tuple, Union

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from utils import exc_log
from utils.config import url_login_strava
from utils.dom_elements import DOMElements

from .credentials import Credentials


class LoginStrava:
    LOGIN_ELEMENTS: List[
        Tuple[
            Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str
        ]
    ] = [
        (EC.visibility_of_element_located, By.ID, "email"),
        (EC.visibility_of_element_located, By.ID, "password"),
        (EC.element_to_be_clickable, By.CSS_SELECTOR, "button.btn.btn-primary"),
    ]

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the LoginStrava object.

        Args:
            driver (WebDriver): The WebDriver object to be used for interacting with the browser.
        """
        self.driver: WebDriver = driver
        self.element = DOMElements(driver)

    def login(self) -> None:
        """
        Perform the login process.

        This method opens the login URL, fills in the email and password fields, and clicks the login button.
        """
        try:
            self.element.open_url(url=url_login_strava)
            elements: List[WebElement] = [
                self.element.find_element(*element) for element in self.LOGIN_ELEMENTS
            ]
            email_field, password_field, login_button = elements

            self.element.fill_field(element=email_field, value=Credentials.email)
            self.element.fill_field(element=password_field, value=Credentials.password)
            self.element.click_button(element=login_button)

        except (TimeoutError, Exception) as e:
            exc_log.exception(f"Error:  {e}")
