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

from config import (
    EMAIL,
    PASSWORD,
    seconds,
    url_to_get_OAuth_code
)
from logger.logger import ErrorLogger
from src.correct_elevation.credentials import Credentials
from src.correct_elevation.strava import Strava

logger = ErrorLogger()


class GetCode:

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
        except Exception:
            return False

    def get_code_from_url(self, driver: WebDriver) -> str:
        authorizated_url = driver.current_url
        code_regex = re.compile("&code=([\a-z]+)&")
        code_match = code_regex.search(authorizated_url)

        if not code_match:
            logger.error("Could not retrieve OAuth code from URL")

        return code_match.group(1)


OAuth_page = GetCode()


def get_oauth_code() -> str:
    """
    Launches a web browser to retrieve the OAuth code from Strava.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    with webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    ) as driver:
        driver.implicitly_wait(seconds)
        driver.get(url_to_get_OAuth_code)
        try:
            credentials = Credentials(EMAIL, PASSWORD)
            strava = Strava(driver)
            strava.login(credentials)
            print("TEST1 LOG in")
            if OAuth_page.click_authorize(driver):
                print("TEST2: CLICK")
                code = OAuth_page.get_code_from_url(driver)
                return code
        except Exception as e:
            logger.error(f"Error: {e}")
