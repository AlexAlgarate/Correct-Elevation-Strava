import re
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from typing import Literal
from config import strava_login_url
from src.correct_elevation.credentials import Credentials
from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import \
    GetOauthCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import \
    LoginStrava


@pytest.fixture
def valid_credentials() -> Credentials:
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def invalid_email() -> str:
    return "example123example.com"


@pytest.fixture
def empty_credentials() -> Credentials:
    return Credentials("", "")


@pytest.fixture
def strava_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(strava_login_url)
    # sleep(1)
    return driver


@pytest.fixture
def strava_url(strava_driver: WebDriver) -> str:
    return strava_driver.current_url


def test_valid_credentials_instance(valid_credentials: Credentials):
    assert isinstance(valid_credentials, Credentials)


def test_valid_email_format(
    valid_credentials: Credentials, invalid_email: Literal["example123example.com"]
):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    assert re.match(email_regex, valid_credentials.email)
    assert not re.match(email_regex, invalid_email)


def test_empty_credentials_instance(empty_credentials: Credentials):
    assert empty_credentials.email == ""
    assert empty_credentials.password == ""


def test_null_values():
    with pytest.raises(ValueError):
        Credentials(None, None)


def test_code():
    oauth_code = GetOauthCode().get_oauth_code()

    assert oauth_code is not None
    assert isinstance(oauth_code, str)
    assert len(oauth_code) > 0

def test_open_Strava_page(strava_url):
    assert strava_url == strava_login_url


def test_find_email_field(strava_driver):
    assert LoginStrava(strava_driver)._find_element(
        function=EC.visibility_of_element_located,
        locator=By.ID,
        selector="email"
    ) is not None

    assert LoginStrava(strava_driver)._find_element(
        function=EC.visibility_of_element_located,
        locator=By.ID,
        selector="password",
    ) is not None

    assert LoginStrava(strava_driver)._find_element(
        function=EC.element_to_be_clickable,
        locator=By.CSS_SELECTOR,
        selector="button.btn.btn-primary",
    ) is not None
    # assert LoginStrava(driver).login is not None

# TODO

# def test_login_fields(driver):
#     assert LoginStrava(driver)._find_element(
#         function=EC.visibility_of_element_located,
#         locator=By.ID,
#         selector="email"
#     ) is not None
