from __future__ import annotations

import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config import EMAIL, PASSWORD, seconds, url_to_get_OAuth_code
from logger.logger import ErrorLogger
from src.correct_elevation.credentials import Credentials
from src.strava_API.tokens_management.oauth_code_management.login_strava import \
    Strava

logger = ErrorLogger()


class ClickAuthorize:
    """
    Methods:
        - click_authorize() uses Selenium to click on authorize button.
        - extract_code_from_url() uses a regular expression to get the code from the URL

    Attributes:
        - Driver: WebDrivr object
        - web_driver_wait: WebDriverWait object
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def click_authorize(self, driver: WebDriver) -> bool:
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


class ExtractCode:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def extract_code(self, driver: WebDriver) -> str:
        authorizated_url = driver.current_url
        reg_expression = re.compile("&code=([\a-z]+)&")
        code_match = reg_expression.search(authorizated_url)

        if not code_match:
            logger.error("Could not retrieve OAuth code from URL")

        return code_match.group(1)


class GetCode:

    def code_to_get_access_token(self) -> str:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as driver:
            driver.implicitly_wait(seconds)
            try:
                credentials = Credentials(EMAIL, PASSWORD)
                strava = Strava(driver)
                authorize_button = ClickAuthorize(driver)
                get_code = ExtractCode(driver)
                strava.login(credentials)
                driver.get(url_to_get_OAuth_code)
                authorize_button.click_authorize(driver)
                return get_code.extract_code(driver)
            except Exception as e:
                logger.error(f"Error: {e}")
