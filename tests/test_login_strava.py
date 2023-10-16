from typing import Any, List, Tuple, Union

import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils.config import EMAIL, PASSWORD, url_login_strava

WEB_ELEMENTS_TO_FIND: List[
    Tuple[Union[EC.visibility_of_element_located, EC.element_to_be_clickable], By, str]
] = [
    (EC.visibility_of_element_located, By.ID, "email"),
    (EC.visibility_of_element_located, By.ID, "password"),
    (EC.element_to_be_clickable, By.CSS_SELECTOR, "button.btn.btn-primary"),
]


@pytest.fixture
def driver() -> WebDriver:
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = Chrome(service=Service(), options=options)
    yield driver
    driver.quit()


@pytest.fixture
def valid_credentials() -> Credentials:
    return Credentials(EMAIL, PASSWORD)


@pytest.fixture
def wrong_credentials() -> Credentials:
    return Credentials("example123@example.com", "password1234")


@pytest.fixture
def strava_object(driver: WebDriver) -> LoginStrava:
    return LoginStrava(driver)


class TestStravaLoginPage:
    # OK
    def test_strava_isinstances(self, strava_object: LoginStrava, driver: WebDriver) -> None:
        assert isinstance(strava_object, LoginStrava)
        assert isinstance(driver, WebDriver)
        assert hasattr(strava_object, "find_element")
        assert hasattr(strava_object, "click_button")

    # OK
    def test_open_strava_page(self, driver: WebDriver, strava_object: LoginStrava) -> None:
        strava_object.open_url(url_login_strava)
        strava_url: str = driver.current_url
        assert "https://www.strava.com/login" == strava_url

    # OK
    def test_find_elements(self, strava_object: LoginStrava) -> None:
        strava_object.open_url(url=url_login_strava)
        for function, locator, selector in WEB_ELEMENTS_TO_FIND:
            element: Any | None = strava_object.find_element(
                function=function, locator=locator, selector=selector
            )
            assert element is not None

    # TODO
    # def test_login_valaid_credentials(
    #     self,
    #     strava_object: LoginStrava,
    #     valid_credentials: Credentials,
    #     driver: WebDriver,
    # ) -> None:
    #     email_element: Any | None = strava_object.find_element(*WEB_ELEMENTS_TO_FIND[0])
    #     password_element: Any | None = strava_object.find_element(
    #         *WEB_ELEMENTS_TO_FIND[1]
    #     )
    #     login_button: Any | None = strava_object.find_element(*WEB_ELEMENTS_TO_FIND[2])

    #     strava_object.fill_field(email_element, valid_credentials.email)
    #     strava_object.fill_field(password_element, valid_credentials.password)
    #     strava_object.click_button(login_button)
    #     time.sleep(1)

    #     assert email_element.get_attribute("value") == valid_credentials.email
    #     assert password_element.get_attribute("value") == valid_credentials.password
    #     assert "https://www.strava.com/dashboard#_=_" == driver.current_url
