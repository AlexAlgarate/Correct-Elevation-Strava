import os
import sys
from typing import Any, List, Tuple, Union

import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.correct_elevation.strava_activity import StravaActivity
from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils.config import url_OAuth

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import (
    OauthCodeGetter,
)

WEB_ELEMENTS_TO_FIND: List[Tuple[EC.element_to_be_clickable, By, str]] = [
    (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button#authorize",
    )
]

authorization_url: str = "https://www.strava.com/oauth/authorize"
response_type: str = "response_type=code"
redirect_url: str = "http://localhost/exchange_token"
redirect_uri: str = f"redirect_uri={redirect_url}"
client_id_env: str = "STRAVA_CLIENT_ID"
approval_prompt: str = "approval_prompt=force"
CLIENT_ID: int = int(os.getenv(client_id_env))
client_id: str = f"client_id={CLIENT_ID}"
scopes: str = "read,read_all,activity:read,activity:read_all"
scope: str = f"scope={scopes}"

# url_OAuth: str = f"{authorization_url}?{client_id}&{response_type}&{redirect_uri}&{approval_prompt}&{scope}"


@pytest.fixture
def strava_driver() -> WebDriver:
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = Chrome(service=Service(), options=options)
    # driver.get(url_OAuth)
    yield driver
    driver.quit()


class TestOauthCode:
    def setup_method(self, strava_driver: WebDriver):
        self.strava_login = LoginStrava(strava_driver)

    # def setup_method(self) -> str:
    #     self.oauth_code: str = OauthCodeGetter().get_oauth_code()
    #     return self.oauth_code

    # it works
    # def test_open_code_url(self, strava_driver: WebDriver, login_strava) -> None:
    #     login_strava
    #     strava_driver.get(url=url_OAuth)
    #     assert (
    #         strava_driver.current_url
    #         == "https://www.strava.com/oauth/authorize?client_id=89686&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read,read_all,activity:read,activity:read_all"
    #     )

    # it works
    # def test_login_tries_exceeded(self, strava_driver: WebDriver) -> None:
    #     strava_driver.get(url=url_OAuth)
    #     assert strava_driver.current_url == "https://www.strava.com/login"
    #     assert url_OAuth != strava_driver.current_url

    # def test_find_elements(self, strava_driver: WebDriver) -> None:
    #     self.strava_login.login()
    #     self.strava_login.open_login_url(url=url_OAuth)
    #     # strava_driver.get(url=url_OAuth)
    #     for function, locator, selector in WEB_ELEMENTS_TO_FIND:
    #         element: Any | None = self.strava_login.find_element(
    #             function=function, locator=locator, selector=selector
    #         )
    #         assert element is not None

    # def test_code(self) -> None:
    #     assert self.oauth_code is not None
    #     assert isinstance(self.oauth_code, str)
    #     assert len(self.oauth_code) > 0
