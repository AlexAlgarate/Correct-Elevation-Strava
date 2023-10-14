from typing import List, Tuple, Union

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.config import url_login_strava
from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava

WEB_ELEMENTS_TO_FIND: List[
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str]
] = [
    (EC.visibility_of_element_located, By.ID, "email"),
    (EC.visibility_of_element_located, By.ID, "password"),
    (EC.element_to_be_clickable, By.CSS_SELECTOR, "button.btn.btn-primary"),
]


@pytest.fixture
def strava_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(url_login_strava)
    yield driver
    driver.quit()


@pytest.fixture
def valid_credentials() -> Credentials:
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def login_strava(strava_driver: WebDriver):
    return LoginStrava(strava_driver)


class TestStravaLoginPage:
    def test_open_strava_page(self, strava_driver: WebDriver):
        assert strava_driver.current_url == url_login_strava

    def test_find_elements(self, strava_driver: WebDriver):
        for function, locator, selector in WEB_ELEMENTS_TO_FIND:
            element = LoginStrava(strava_driver)._find_element(
                function=function, locator=locator, selector=selector
            )
            assert element is not None

    def test_fill_fields(
        self, login_strava: LoginStrava, valid_credentials: Credentials
    ):
        email_element = login_strava._find_element(*WEB_ELEMENTS_TO_FIND[0])
        password_element = login_strava._find_element(*WEB_ELEMENTS_TO_FIND[1])

        login_strava._fill_field(email_element, valid_credentials.email)
        login_strava._fill_field(password_element, valid_credentials.password)

        assert email_element.get_attribute("value") == valid_credentials.email
        assert password_element.get_attribute("value") == valid_credentials.password
