from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import OauthCodeGetter
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils.config import (
    CLIENT_ID,
    OAuth_url,
    approval_prompt,
    authorization_url,
    client_id,
    redirect_uri,
    response_type,
    scope,
)
from utils.locators import oauth_elements
from utils.web_element_handler import WebElementHandler


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

    def test_access_oauth_code_url_when_no_logged_in(self, driver: Chrome) -> None:
        driver.get(url=OAuth_url)
        assert driver.current_url == "https://www.strava.com/login"
        assert OAuth_url != driver.current_url

    def test_access_oauth_code_url(
        self, driver: Chrome, element: WebElementHandler, login_strava: LoginStrava
    ) -> None:
        # Check if accessing OAuth URL after login is successful
        login_strava
        driver.get(url=OAuth_url)
        expected_url: str = (
            "https://www.strava.com/oauth/authorize?"
            f"client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read,read_all,activity:read,activity:read_all"
        )
        assert driver.current_url == expected_url

        # Find the authorize_button
        authorize_button: WebElement = element.find_element(*oauth_elements["authorize_button"])
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
