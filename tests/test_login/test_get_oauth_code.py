from typing import Dict, Tuple, Union

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import (
    OauthCodeGetter,
)
from utils.config import (
    authorization_url,
    client_id,
    response_type,
    redirect_uri,
    approval_prompt,
    scope,
    OAuth_url,
)
from utils.web_element_handler import WebElementHandler
from .test_config import driver, login_strava, element


OAUTH_WEB_ELEMENTS: Dict[str, Tuple[Union[EC.element_to_be_clickable, By, str]]] = {
    "authorize_button": (
        EC.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button#authorize",
    )
}


class TestOauthCode:
    def test_construct_oauth_url(self):
        expected_url: str = (
            f"{authorization_url}?"
            f"{client_id}&"
            f"{response_type}&"
            f"{redirect_uri}&"
            f"{approval_prompt}&"
            f"{scope}"
        )
        assert expected_url == OAuth_url

    def test_access_oauth_code_url_when_no_logged_in(self, driver) -> None:
        driver.get(url=OAuth_url)
        assert driver.current_url == "https://www.strava.com/login"
        assert OAuth_url != driver.current_url

    def test_access_oauth_code_url(
        self, driver: WebDriver, element: WebElementHandler, login_strava
    ) -> None:
        # Check if accessing OAuth URL after login is successful
        login_strava
        driver.get(url=OAuth_url)
        expected_url: str = (
            "https://www.strava.com/oauth/authorize?"
            "client_id=89686&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read,read_all,activity:read,activity:read_all"
        )
        assert driver.current_url == expected_url

        # Find the authorize_button
        authorize_button: WebElement = element.find_element(*OAUTH_WEB_ELEMENTS["authorize_button"])
        assert authorize_button is not None

        # Click on the authorize_button
        element.click_button(authorize_button)

        # Check if the URL with the OAuth code matches the expected format
        url_with_oauth_code: str = "http://localhost/exchange_token?state=&code=a9ac7dc9ccfb13678d2f3c0104d8fdc8fdb72193&scope=read,activity:read,activity:read_all,read_all"
        assert driver.current_url.startswith(url_with_oauth_code[:44])

    def test_code_properties(self):
        code = OauthCodeGetter().get_oauth_code()
        assert code is not None
        assert isinstance(code, str)
        assert len(code) > 0
